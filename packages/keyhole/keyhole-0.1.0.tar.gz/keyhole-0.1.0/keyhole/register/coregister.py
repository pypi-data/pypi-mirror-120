from itertools import groupby
import logging
from pathlib import Path

import numpy as np
from skimage import io, measure, transform, filters

from .phase_cross_correlation import phase_cross_correlation
from ..platforms import platform_for_image, approx_panel_overlap


log = logging.getLogger("cast.keyhole.coregister")


def coregister_all(paths):
    """Coregister all given panels."""

    all_tforms = {}

    # Group panels by everything up to the "_[abcd].tif"
    for k, g in groupby(paths, key=lambda p: str(p)[:-6]):
        name = Path(k).name
        all_tforms[name] = coreg_image(k, list(g))

    return all_tforms


def prettify_transform(tform) -> str:
    shift = np.array2string(
        tform.translation, precision=2, sign="+", suppress_small=True
    )
    return f"{shift} {np.degrees(tform.rotation):+0.5f} deg"


def coreg_image(name, panel_paths, overlap=None):
    """Coregister the panels belonging to a single Corona image."""
    log.info(name)

    if not overlap:
        platform = platform_for_image(name)
        overlap = approx_panel_overlap(platform)
    if not overlap:
        raise RuntimeError(f"Can't guess platform for image {name}")

    panel_tforms = {}

    this_panel = io.imread(panel_paths[0])
    this_id = panel_paths[0].stem[-1]
    for path in panel_paths[1:]:
        next_panel = io.imread(path)
        next_id = path.stem[-1]
        log.info(f"{next_id} to {this_id}")

        tform = coregister_panels(this_panel, next_panel, overlap)
        log.info(prettify_transform(tform))
        panel_tforms[this_id, next_id] = tform.params

        this_panel = next_panel
        this_id = next_id

    return _register_to_left(panel_tforms)


def _register_to_left(panel_tforms):
    """Register all panels to the leftmost panel.

    Given transforms that register b to a, c to b, etc, multiply through so
    that the leftmost panel transform is identity, and the others transform
    from their respective panels into the left panel's coordinates.
    """
    # All of the panel names (a, b, ...) involved in the transforms.
    panels = sorted(list(set(panel for pair in panel_tforms.keys() for panel in pair)))

    # The column offset of any transform tells us the panel order.
    arbitrary_tform = list(panel_tforms.values())[0]
    right_to_left = arbitrary_tform[1, 2] <= 0
    if right_to_left:

        # Put panel names in left-to-right order.
        panels = panels[::-1]

        # Get the right-to-left transforms.
        original_keys = list(panel_tforms.keys())
        for dst, src in original_keys:
            panel_tforms[src, dst] = np.linalg.inv(panel_tforms[dst, src])

    # The leftmost panel transform is identity.
    to_leftmost = {panels[0]: np.eye(3)}

    # Multiply through with the adjacent panel transforms.
    for left, right in zip(panels, panels[1:]):
        to_leftmost[right] = to_leftmost[left] @ panel_tforms[left, right]

    return to_leftmost


def coregister_panels(
    panel_a: np.array,
    panel_b: np.array,
    overlap: int,
    chip_size: int = 100,
    max_matches: int = 1000,
) -> transform.EuclideanTransform:
    """Coregister a single pair of panel images.

    This can succeed, outright fail, or be weak enough to merit review. The
    function could be improved by returning additional information along those
    lines in addition to the transform. But for now, it simply logs those
    conditions.

    Note that this uses stochastic processes, so multiple calls with the same
    arguments will return slightly varying results.

    Returns
    -------
    tform: scikit.transform.EuclideanTransform
        Transforms panel_b coordinates into panel_a coordinates.
    """
    # Get an initial estimate of the transform. This tends to be accurate to
    # 5–10 pixels.
    approx_tform = estimate_coregistration(panel_a, panel_b, overlap)

    # Make a grid of matches based on the intial estimate.
    pts_a, pts_b = get_overlapping_grid(panel_a, panel_b, approx_tform, chip_size)

    # Identify and refine good matches.
    pts_a, pts_b = find_matches(panel_a, panel_b, pts_a, pts_b, max_matches, chip_size)

    # You need two pairs of points to estimate a Euclidean transformation.
    num_matches = len(pts_a)
    if num_matches < 2:
        log.error(f"FAILED: {num_matches} matches")
        return transform.EuclideanTransform(rotation=np.nan)

    # Fit a new transform to the matched points.
    tform, inliers = measure.ransac(
        data=(pts_b, pts_a),
        model_class=transform.EuclideanTransform,
        min_samples=2,
        residual_threshold=1.0,
    )

    num_inliers = np.count_nonzero(inliers)

    if num_inliers < 8:
        log.warning(f"PROBABLY FAILED: inliers/matches: {num_inliers} / {num_matches}")
    elif num_inliers / num_matches < 0.5 or num_matches < 100:
        log.warning(f"POSSIBLY FAILED: inliers/matches: {num_inliers} / {num_matches}")
    else:
        log.info(f"inliers/matches: {num_inliers} / {num_matches}")

    return tform


def estimate_coregistration(
    panel_a: np.array,
    panel_b: np.array,
    overlap: int,
) -> transform.EuclideanTransform:
    """Make an initial estimate of the transformation between two panels.

    Parameters
    ----------
    panel_a:
        image data
    panel_b:
        image data
    overlap:
        approximate expected horizontal overlap in pixels

    Returns
    -------
    scikit.transform.EuclideanTransform
        Transforms panel_b coordinates into panel_a coordinates.
    """
    nrows_a, ncols_a = panel_a.shape
    nrows_b, ncols_b = panel_b.shape

    # PCC can only return a shift of up to half the image dimensions, so we
    # cannot use it directly on the panel images, which only overlap at the
    # edges. Instead, try both a left-to-right and a right-to-left order, using
    # the left and right parts of each image. Then, use the ordering with
    # less correlation error.

    # The size of the overlapping regions, which must be equal for PCC.
    nrows = min(nrows_a, nrows_b)
    ncols = min(overlap, ncols_a, ncols_b)

    # The overlapping subimages from panel_a and panel_b, keyed by order. For
    # example, overlap_a["ab"] is the right portion of panel_a.
    overlap_a, overlap_b = {}, {}

    # Downsample the overlapping regions; at their original size, this routine
    # is too slow. Downsampling beyond a factor of four seems to make the
    # registration process less reliable.
    scale = 4

    # This downsampling is a compromise between correctness and performance.
    # The exact solution is to simply use pyramid_reduce at the desired scale.
    # On the large panel images, that takes a while. The fastest solution is to
    # simply decimate, i.e. ``img[::scale, ::scale]``, but that introduces a
    # lot of noise into the downsampled image.
    overlap_a["ab"] = transform.pyramid_reduce(panel_a[:nrows:2, -ncols::2], scale // 2)
    overlap_b["ab"] = transform.pyramid_reduce(panel_b[:nrows:2, :ncols:2], scale // 2)
    overlap_a["ba"] = transform.pyramid_reduce(panel_a[:nrows:2, :ncols:2], scale // 2)
    overlap_b["ba"] = transform.pyramid_reduce(panel_b[:nrows:2, -ncols::2], scale // 2)

    # Record the offset of the overlaps from the full image.
    offset_a, offset_b = {}, {}
    offset_a["ab"] = np.array([0, (ncols_a - ncols)])
    offset_b["ab"] = np.array([0, 0])
    offset_a["ba"] = np.array([0, 0])
    offset_b["ba"] = np.array([0, (ncols_b - ncols)])

    # Pick the order based on which PCC calculation produces less error.
    delta, err = {}, {}
    for order in "ab", "ba":
        delta[order], err[order], _, _ = phase_cross_correlation(
            overlap_a[order], overlap_b[order], upsample_factor=scale * 5
        )
    order = "ab" if err["ab"] < err["ba"] else "ba"

    pretty_order = "left, right" if order == "ab" else "right, left"
    log.debug(f"guessed order: {pretty_order}")

    # TODO: more docs here
    est_shift = offset_a[order] + np.array(delta[order]) * scale - offset_b[order]
    pretty_shift = np.array2string(est_shift, precision=0, suppress_small=True)
    log.debug(f"guessed shift: {pretty_shift}")

    # Having found the correct overlaps, split them into top and bottom halves.
    # We will seperately coregister these to give us two point correspondances,
    # which we can use to estimate a Euclidean transformation.
    top, bot = 0, 1
    nrows_top = overlap_a[order].shape[0] // 2
    for overlap in overlap_a, overlap_b:
        overlap[top] = overlap[order][:nrows_top]
        overlap[bot] = overlap[order][nrows_top:]

    for offset in offset_a, offset_b:
        offset[top] = offset[order]
        offset[bot] = offset[order] + np.array([nrows_top, 0]) * scale

    pts_a, pts_b = np.zeros((2, 2)), np.zeros((2, 2))
    for half in top, bot:
        # For large, heterogeneous areas of the image, low frequency effects
        # (large areas of the image being predominantly light or dark) can
        # dominate the PCC and prevent accurate correlation. Removing the low
        # frequency information is effectively an edge detector.
        edges_a = overlap_a[half] - filters.gaussian(overlap_a[half], 4)
        edges_b = overlap_b[half] - filters.gaussian(overlap_b[half], 4)

        delta[half], err[half], _, _ = phase_cross_correlation(
            edges_a, edges_b, upsample_factor=scale * 5
        )

        # Find the centers of each overlap section in the original image
        # coordinates.
        a_center = np.array(overlap_a[half].shape) / 2
        pts_a[half] = a_center * scale + offset_a[half]
        b_center = np.array(overlap_b[half].shape) / 2
        pts_b[half] = (b_center - delta[half]) * scale + offset_b[half]

    log.debug(f"top shift: {delta[top]}")
    log.debug(f"bot shift: {delta[bot]}")

    tform = transform.estimate_transform("euclidean", pts_b, pts_a)
    log.debug(f"initial estimate: {prettify_transform(tform)}")
    return tform


def get_overlapping_grid(
    panel_a: np.array,
    panel_b: np.array,
    approx_tform: transform.EuclideanTransform,
    chip_size: int,
):
    """Create a grid of points that should roughly match in each image.

    Returns
    -------
    grid_a: np.array
        (n x 2) array of row, col points
    grid_b: np.array
        (n x 2) array of row, col points that match the points in grid_a
        based on approx_tform
    """
    nrows_a, ncols_a = panel_a.shape
    nrows_b, ncols_b = panel_b.shape
    half_chip = chip_size // 2

    # Make a regular grid of points in the panel_a image such that, if each
    # point is the center of a chip_size x chip_size square, no chips would
    # overlap and all chips are completely inside the image.
    rr, cc = np.mgrid[
        half_chip : nrows_a - half_chip : chip_size,
        half_chip : ncols_a - half_chip : chip_size,
    ]
    grid_a = np.array((rr.ravel(), cc.ravel())).T

    # Project the grid into panel_b. grid_a is naturally of type int, convert
    # grid_b to the same: we need integer coordinates for slicing elsewhere.
    grid_b = approx_tform.inverse(grid_a).astype(int)

    # Filter both grids based on which points are in a valid area of panel_b.
    mask = (
        (grid_b[:, 0] > half_chip)
        & (grid_b[:, 0] < nrows_b - half_chip)
        & (grid_b[:, 1] > half_chip)
        & (grid_b[:, 1] < ncols_b - half_chip)
    )
    grid_a = grid_a[mask]
    grid_b = grid_b[mask]

    return grid_a, grid_b


def find_matches(
    panel_a: np.array,
    panel_b: np.array,
    pts_a: np.array,
    pts_b: np.array,
    max_matches: int = 1000,
    chip_size: int = 100,
):
    """Given rough matches, find accurate matches in overlapping images.

    Arguments
    ---------
    panel_a: array
        reference image
    panel_b: array
        overlapping image
    pts_a: (n, 2) array
        row, col points in panel_a
    pts_b: (n, 2) array
        row, col points in panel_b matching corresponding to pts_a
    max_matches: int
        return up to this many matches
    chip_size: int
        the neighborhood around each point is a square chip_size pixels on each
        side.

    Returns
    -------
    good_pts_a: (m, 2) array
        points from pts_a with a good match to b
    good_pts_b: (m, 2) array
        points in b matching good_pts_a
    """
    # Since we will likely find num_matches fairly quickly, shuffle the grids
    # so that the first matches are spread across the overlap area, instead of
    # just at the top.
    rng = np.random.default_rng()
    p = rng.permutation(len(pts_a))
    grid_a = pts_a[p]
    grid_b = pts_b[p]

    # Build up matches until you find the requested number of matches or run
    # out of grid points.
    matched_a = []
    matched_b = []
    for pt_a, pt_b in zip(grid_a, grid_b):
        pt_b_refined = refine_match(panel_a, panel_b, pt_a, pt_b, chip_size)

        if pt_b_refined is not None:
            matched_a.append(pt_a)
            matched_b.append(pt_b_refined)

        if len(matched_a) >= max_matches:
            break

    return np.array(matched_a), np.array(matched_b)


def refine_match(
    ref_image, match_image, ref_point, match_start, chip_size=100, max_rmse=0.3
):
    """
    Turn a rough point match into a precise match.

    Arguments
    ---------
    ref_image : array
        image data
    match_image : array
        image data
    ref_point : (2, 1) array of int
        A point in `ref_image` inset from the image edge at least
        `chip_size // 2` rows and cols.
    match_start : (2, 1) array of int
        A point near where `match_image` matches `ref_image`, inset from the
        image edge at least `chip_size // 2` rows and cols.
    chip_size : int
        An area of the image around each point of size (`chip_size`,
        `chip_size) will be used. This value needs to be much larger than the
        expected error in the location of `match_start`, but larger size
        increases execution time and might lose precision.
    max_rmse: float
        The maximum rmse phase error before returning no match. The default
        value works for KH-4 and KH-9.

    Returns
    -------
    match_improved: (1, 2) array or None
        A point near `match_start` in `match_image` that most closely matches
        `ref_point` in `ref_image`. Returns None if the function could not
        refine the match with high confidence.
    """
    ref_row, ref_col = ref_point
    match_row, match_col = match_start
    chip_half = chip_size // 2

    # Slice the point neighborhoods out of the images.
    ref_chip = ref_image[
        ref_row - chip_half : ref_row + chip_half,
        ref_col - chip_half : ref_col + chip_half,
    ]
    match_chip = match_image[
        match_row - chip_half : match_row + chip_half,
        match_col - chip_half : match_col + chip_half,
    ]

    if not (_is_good_chip(ref_chip) and _is_good_chip(match_chip)):
        return None

    (shift_row, shift_col), error, _, pcc = phase_cross_correlation(
        ref_chip, match_chip, upsample_factor=100
    )

    # Sometimes, the PCC result can be improved by smoothing the chips.
    # However, _in general_ this makes the PCC results less accurate. So, only
    # retry the PCC with smoothing if the match would otherwise be rejected.
    if error > max_rmse:
        ref_chip = filters.gaussian(ref_chip)
        match_chip = filters.gaussian(match_chip)
        (shift_row, shift_col), error, _, pcc = phase_cross_correlation(
            ref_chip, match_chip, upsample_factor=100
        )

    if not _is_localized(pcc) or error > max_rmse:
        return None

    return np.array([match_row - shift_row, match_col - shift_col])


def _is_good_chip(chip, min_range=10, min_value=15, min_ratio=0.01):
    """Check if an image chip is suitable for PCC.

    This function performs several checks. They are all based on empirical
    testing; i.e., they were developed by simply looking at a lot of image
    chips and seeing where PCC fails. The default arguments are based on that
    testing, which means that they, and possibly this whole function, are only
    valid for the types of images it was tested on: KH-4 and KH-9.
    """
    # Image chips with a low range of values work poorly. This covers:
    # - All zeroes, which make PCC throw an exception
    # - Homogenous chips, which fail because there's no phase information.
    # - Nearly-homogenous chips, typically in margins, over water, or over
    #   snowpack, that always fail to produce a localized result.
    if np.ptp(chip) < min_range:
        return False

    # If a chip is mostly dark with just a few bright pixels, it will pass the
    # test above. However, such chips are usually a speck of dust or lint in
    # the margins. Two such chips might strongly match, but they're actually
    # looking at different specks of dust, so the match will be spurious.
    if np.count_nonzero(chip >= min_value) < chip.size * min_ratio:
        return False

    return True


def _is_localized(pcc, threshold=0.8, furthest=15.0):
    """Test if a PCC result is well-localized.

    This function, and its default arguments, are based on testing on KH-4 and
    KH-9 images, and probably aren't suitable for other types of images.
    """
    cc = np.abs(pcc)

    # The PCC wraps at the edges. Roll the maximum PCC response value to the
    # middle to simplify distance calculation.
    this_max = np.array(np.unravel_index(np.argmax(cc), cc.shape))
    this_middle = np.array(cc.shape) // 2
    this_roll = this_middle - this_max
    rolled_cc = np.roll(cc, this_roll, (0, 1))

    # Normalize PCC to [0, 1].
    min_cc = np.min(cc)
    max_cc = np.max(cc)
    range_cc = max_cc - min_cc
    rolled_cc = (rolled_cc - min_cc) / range_cc

    # Find all PCC responses over the threshold, and get their distance to the
    # maximum response.
    biguns = np.argwhere(rolled_cc > threshold)
    distances = np.linalg.norm(biguns - this_middle, axis=1)

    return np.max(distances) <= furthest


if __name__ == "__main__":
    main()
