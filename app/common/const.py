from model_utils import Choices


WEBSITE_STATUSES = Choices(
    ('Sta', "started", "Started"),
    ('Tpr', "getting_text", "Getting the text in progress"),
    ('Ipr', "getting_images", "Getting images in progress"),
    ('Suc', "success", "Success"),
    ('Fai', "failed", "Failed"),
)
