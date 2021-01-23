import cv2 as cv


def match_template(template, source, resize=True, match_threshold=0.8, debug_show=False):
    template_img = cv.imread(template)
    # Mac的Retina屏幕截取的图片会出现分辨率不匹配的问题，需要压缩才能正常匹配
    if resize:
        template_img = cv.resize(template_img, (0, 0), fx=0.5, fy=0.5)
    source_img = cv.imread(source)
    match_result = cv.matchTemplate(source_img, template_img, cv.TM_CCOEFF_NORMED)
    min_val, max_val, br_loc, tl_loc = cv.minMaxLoc(match_result)
    if debug_show:
        print("match result for ", template, " in ", source, (min_val, max_val, br_loc, tl_loc))
    if max_val > match_threshold and debug_show:
        corner_loc = (tl_loc[0] + template_img.shape[1], tl_loc[1] + template_img.shape[0])
        center_spot = (tl_loc[0] + int(template_img.shape[1] / 2), tl_loc[1] + int(template_img.shape[0] / 2))
        cv.circle(source_img, center_spot, 10, (0, 255, 255), -1)
        cv.rectangle(source_img, tl_loc, corner_loc, (0, 0, 255), 3)
        if debug_show:
            cv.imshow("MatchResult", source_img)
            cv.waitKey(2000)
    return max_val, br_loc, tl_loc
