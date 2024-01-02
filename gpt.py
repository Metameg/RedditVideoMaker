import utils
from openai import OpenAI

class GPT():
	def __init__(self, msg, title):
		self.settings = utils.read_config()
		self.client = OpenAI(api_key=self.settings['gpt']['api_key'])
		self.content = msg
		self.title = title
		self.new_story = ""
	
	def recreate_story(self):
		print(self.content)
		print(self.title)
		response = self.client.chat.completions.create(
			model="gpt-3.5-turbo",
			messages=[
				{"role": "system", "content": "Your job is to re-word stories given to you from reddit and make them captivating."},
				{"role": "system", "content": "The stories you will receive will have a particular meaning and intent by the story teller. Maintaining the intent of the original story is the most important thing here and should remain a priority."},
				{"role": "system", "content": "Any curse words or inappropriate language should be censored in the new story you are creating."},
				{"role": "system", "content": "Ensure that the re-worded content remains engaging, captivating, and relevant to the topic while maintaining clarity and coherence."},
				{"role": "system", "content": "Ensure that the reworded content is easy to understand for a broad audience while retaining the subject's technical or specific aspects."},
				{"role": "system", "content": "Inject creativity and engagement into the reworded content to make it more appealing to readers. This can include storytelling elements, questions, or prompts for comments."},
				{"role": "user", "content": f'The story you will recreate is {self.content}. Make sure the story you re-write is between 1200 and 2100 characters long. This length should be a priority.'},
				{"role": "user", "content": "The story is way too long. Make sure you stick to the 1200 to 1600 character limit."}
			]
		)

		self.new_story = response.choices[0].message.content
		return self.new_story

	def recreate_title(self):

		response = self.client.chat.completions.create(
			model="gpt-3.5-turbo",
			messages=[
				{"role": "system", "content": "You are given a story that needs to be briefly summarized in 10-20 words. The length of this summary should remain a top priority."},
				{"role": "system", "content": "The goal of this summary is to highlight the most dramatic and shocking parts of the story. Keep the language of this summary at a sixth grade vocabulary."},
				{"role": "system", "content": "The summary should fit well as the opening sentence to the story. Retain a first person point of view for the summary."},
				{"role": "user", "content": f'The summary you will create is from the following story: {self.new_story}'},
				{"role": "assistant", "content": "In our early twenties, I fell for Lily, but she rejected me. Years later, we reconnected, but she still only saw me as a friend. Now, she asked me to help her son, but I hesitated, and she cut me out of her life."},
				{"role": "user", "content": "The summary you are giving me is too wordy. Make sure you stick to the 10-20 word limit."},
				{"role": "assistant", "content": "Rejected twice by Lily, reconnected as friends, but when asked to help her son, she cut me out."},
				{"role": "user", "content": "Avoid using proper nouns in the summary."}
			]
		)

		return response.choices[0].message.content

# if __name__ == '__main__':
# 	msg = '''I (16f) am in a friend group with around 8 people and one person in particular im really good friends with,let's call her anna (15f).Many girls in our class call our friendship weird since we play around by strangling eachother seeing how long we can last,tripping eachother over etc. stuff like this is normal for us.One Monday in PE we got changed and went to our gym where two classes got split into boys and girls.All the boys got sent out to the other sports hall and all the girls were talking to the female PE teacher about what sport they'd like to do.I was running around anna ,since I was hyper after lunch, and messing with her.I quickly tugged at her trousers to scare her but her trousers actually came down to her knees.She seemed annoyed and she ended up tackling me to the ground and strangling me.And btw only one person saw what happened and they are close friends to anna so they wouldn't judge her or anything.But this is were things went wrong.She seemed annoyed at me at first but then when we started doing sports she seemed fine.But when changing she seemed really distant.I sent her an apology over text but she didnt read it or answer.The next day she refused to talk to me or even look at me.She told our form tutor what happened and so did I and he was obviously on her side and said she needs some time alone to think about what happened.So I though alright I'll give her some time and then I'll ask if we could have a meeting with me,anna and our teacher to sort things out but a week has passed and she still refuses to talk and look at me plus she even refused the meeting.I hate her for this because if we don't talk nothing will get sorted out.Annas friend told me I should respect Anna's decision to never be friends with me again.All the people in our friendship group think Anna's overreacting a bit and are hoping she'll be friends with me again but the way things are going I don't think she'll even acknowledge my existence in along time.'''
# 	gpt = GPT( msg, "AITA for feeling guilty about sending my ex bff to prison?" )
# 	gpt.recreate_story()
# 	gpt.recreate_title()

