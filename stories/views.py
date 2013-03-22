import datetime

from django.template import loader, Context
from django.http import HttpResponse
from django.utils.timezone import utc

from stories.models import Story

def score(story, gravity=1.8, timebase=120):
	points = (story.points - 0)**0.8
	now = datetime.datetime.utcnow().replace(tzinfo=utc)
	age = int((now - story.created_at).total_seconds())/60

	return points/(age+timebase)**1.8

def top_stories(top=180, consider=1000):
	lastest_stories = Story.objects.all().order_by('-created_at')[:consider]
	ranked_stories = sorted([(score(story), story) for story in lastest_stories], reverse=True)
	return [story for _, story in ranked_stories][:top]


def index(request):
	stories = top_stories(top=30)
	template = loader.get_template('index.html')
	context = Context({'stories': stories})
	response = template.render(context)
	return HttpResponse(response)