import cv2 as cv
import lib.base.resources as resources
import lib.base.config as config
import lib.base.logger as logger

special_match_threshold = {
    resources.battle_attack_button: 0.6,
    resources.skill_berserker_sbd: 0.6,
    resources.skill_berserker_azn: 0.6,
    resources.skill_avenger_yste: 0.6,
    resources.battle_click_ui_tip: 0.6
}


def match_template(template, source, resize=True, match_threshold=0.9):
    global special_match_threshold
    if template in special_match_threshold:
        match_threshold = special_match_threshold[template]
    template_img = cv.imread(template)
    # Mac的Retina屏幕截取的图片会出现分辨率不匹配的问题，需要压缩才能正常匹配
    if resize:
        template_img = cv.resize(template_img, (0, 0), fx=0.5, fy=0.5)
    source_img = cv.imread(source)
    match_result = cv.matchTemplate(source_img, template_img, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(match_result)
    template_name = template.replace(config.template_img_path, "")
    logger.log(
        "match {} in {} result is {}, {}".format(template_name, source, (min_val, max_val, min_loc, max_loc),
                                                 match_threshold))
    if max_val > match_threshold and config.currentDebugLevel.value > config.DebugLevel.JUST_LOG.value:
        corner_loc = (max_loc[0] + template_img.shape[1], max_loc[1] + template_img.shape[0])
        center_spot = (max_loc[0] + int(template_img.shape[1] / 2), max_loc[1] + int(template_img.shape[0] / 2))
        cv.circle(source_img, center_spot, 10, (0, 255, 255), -1)
        cv.rectangle(source_img, max_loc, corner_loc, (0, 0, 255), 3)
        if config.currentDebugLevel.value > config.DebugLevel.SAVE_IMG.value:
            cv.imshow("MatchResult", source_img)
            cv.waitKey(2000)
        cv.imwrite(source.replace(".png", "_match.png"), source_img)
    return max_val, max_loc, (max_loc[0] + template_img.shape[1], max_loc[1] + template_img.shape[0])


def has_match(template, source, resize=True, match_threshold=0.9):
    max_val, _, __ = match_template(template, source, resize, match_threshold)
    global special_match_threshold
    if template in special_match_threshold:
        match_threshold = special_match_threshold[template]
    return max_val >= match_threshold


def show_img(path):
    cv.imshow(path, cv.imread(path))
    cv.waitKey()
