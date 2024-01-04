import utils
from openai import OpenAI

class GPT():
	def __init__(self, msg, title=None):
		self.settings = utils.read_config()
		self.client = OpenAI(api_key=self.settings['gpt']['api_key'])
		self.content = msg
		self.title = title
		self.new_story = ""
	
	def recreate_story(self):
		print("Chat GPT is re-creating your story...")
		response = self.client.chat.completions.create(
			model="gpt-3.5-turbo",
			messages=[
				{"role": "system", "content": "You are a person that exaggerates and copies short stories as if they happened to you. Your task is to re-word and a story given to you and make it your own in less than 400 words. You will shorten the story into less than 450 words in your response. You will be telling this story in a common conversation."},
				{"role": "system", "content": "The stories you will receive will have a particular meaning and intent by the story teller. Maintaining the intent of the original story is the most important thing here and should remain a priority."},
				{"role": "system", "content": "Any curse words or inappropriate language should be censored in the new story you are creating."},
				{"role": "user", "content": f'This is your story: {self.content}.'},
				{"role": "system", "content": "When you make the story your own, you only add a few embellishments to the story. Make sure to keep your response to less than 400 words,"}
				
			]
		)

		self.new_story = response.choices[0].message.content
		# print(self.new_story)
		return self.new_story

	def recreate_title(self):

		response = self.client.chat.completions.create(
			model="gpt-3.5-turbo",
			# max_tokens=20,
			messages=[
				{"role": "system", "content": "You are a story teller that exaggerates and copies stories as if they happened to you. Your task is to come up with an interesting opening sentence to a story that you are given. This response should explain what happens in the story you are given."},
				{"role": "user", "content": f'This is your story: \n {self.new_story}.\n Create a short opening sentence that is no longer than 20 words for this story.'},
	 			{"role": "system", "content": '''Remember, this story happened to you, so use a first person perspective in this sentence. Also, do not use proper nouns in this response'''},
			]
		)

		print("prompt_tokens: ", response.usage.prompt_tokens)
		print("completion_tokens: ", response.usage.completion_tokens)
		print("total_tokens: ", response.usage.total_tokens)

		return response.choices[0].message.content

if __name__ == '__main__':
	msg = '''I (16f) am in a friend group with around 8 people and one person in particular im really good friends with,let's call her anna (15f).Many girls in our class call our friendship weird since we play around by strangling eachother seeing how long we can last,tripping eachother over etc. stuff like this is normal for us.One Monday in PE we got changed and went to our gym where two classes got split into boys and girls.All the boys got sent out to the other sports hall and all the girls were talking to the female PE teacher about what sport they'd like to do.I was running around anna ,since I was hyper after lunch, and messing with her.I quickly tugged at her trousers to scare her but her trousers actually came down to her knees.She seemed annoyed and she ended up tackling me to the ground and strangling me.And btw only one person saw what happened and they are close friends to anna so they wouldn't judge her or anything.But this is were things went wrong.She seemed annoyed at me at first but then when we started doing sports she seemed fine.But when changing she seemed really distant.I sent her an apology over text but she didnt read it or answer.The next day she refused to talk to me or even look at me.She told our form tutor what happened and so did I and he was obviously on her side and said she needs some time alone to think about what happened.So I though alright I'll give her some time and then I'll ask if we could have a meeting with me,anna and our teacher to sort things out but a week has passed and she still refuses to talk and look at me plus she even refused the meeting.I hate her for this because if we don't talk nothing will get sorted out.Annas friend told me I should respect Anna's decision to never be friends with me again.All the people in our friendship group think Anna's overreacting a bit and are hoping she'll be friends with me again but the way things are going I don't think she'll even acknowledge my existence in along time.'''
	gpt = GPT( msg )
	story = gpt.recreate_story()
	title = gpt.recreate_title()
<<<<<<< HEAD
=======

	print(title  + story)


>>>>>>> 7400e5382c55a00d047ab0a1f4259795c44da7ed

	print(title  + story)