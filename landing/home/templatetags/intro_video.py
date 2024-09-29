from django import template
from home.models import LandingPage

register = template.Library()

@register.inclusion_tag("home/tags/intro_video.html")
def intro_video():
    home = LandingPage.objects.first()
    video_url = home.video_url
    return {"intro_video": video_url}
