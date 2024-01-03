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
				# {"role": "system", "content": "Your job is to re-word stories given to you from reddit and make them captivating."},
				{"role": "system", "content": "The stories you will receive will have a particular meaning and intent by the story teller. Maintaining the intent of the original story is the most important thing here and should remain a priority."},
				{"role": "system", "content": "Any curse words or inappropriate language should be censored in the new story you are creating."},
				
				# {"role": "system", "content": "Ensure that the re-worded content remains engaging, captivating, and relevant to the topic while maintaining clarity and coherence."},
				# {"role": "system", "content": "Ensure that the reworded content is easy to understand for a broad audience while retaining the subject's technical or specific aspects."},
				# {"role": "system", "content": "Inject creativity and engagement into the reworded content to make it more appealing to readers. This can include storytelling elements, questions, or prompts for comments."},
				{"role": "user", "content": f'This is your story: {self.content}.'},
				{"role": "system", "content": "When you make the story your own, you only add a few embellishments to the story. Make sure to keep your response to less than 400 words,"}
				# {"role": "user", "content": "The story is way too long. Make sure you stick to the 1200 to 1600 character limit."}
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
				# {"role": "system", "content": '''You are asked to summarize a story in one sentence that is no more than 20 words.'''}, 
				# {"role": "system", "content": '''Do not use words like "he", "she", or "they" in your response. Instead, use words like "I" and "Me" to maintain a first person point of view'''},
				# {"role": "system", "content": "The goal of this summary is to highlight the most dramatic and shocking parts of the story. Keep the language of this summary at a sixth grade vocabulary."},
				# {"role": "system", "content": "The summary should fit well as the opening sentence to the story."},
				# {"role": "system", "content": "Do not use proper nouns in the summary."},
				# {"role": "user", "content": f'The summary you will create is from the following story: {self.new_story}'},
				{"role": "system", "content": "You are a story teller that exaggerates and copies stories as if they happened to you. Your task is to come up with an interesting opening sentence to a story that you are given. This response should explain what happens in the story you are given."},
				{"role": "user", "content": f'This is your story: \n {self.new_story}.\n Create a short opening sentence that is no longer than 20 words for this story.'},
	 			{"role": "system", "content": '''Remember, this story happened to you, so use a first person perspective in this sentence. Also, do not use proper nouns in this response'''},
				#  {"role": "system", "content": '''Keep the language used in your response simplified so that a child can understand it.'''},
	 			# {"role": "system", "content": "Follow this example summary:\n I kicked out my spoiled daughter because she can't close her legs. I can't handle a 7th child in one room. I have a 27-year-old daughter. She has six kids between the ages ten years old to eleven months old. She has three baby daddies. Two of them give her child support and the third she's been casually dating for five years. They've lived with us for the past year after they got evicted from their last home. Due to my daughter having a part-time job and her  being a tortured artist, I have literally no space for their huge family. Apart from my bedroom and the basic rooms every house needs, there's only two bedrooms available for them. My daughter and her boy toy took one of the bedrooms while the six kids share the other bedroom. These poor kids barely even have any space to themselves. Each of them have to share a bed and the oldest often have to take care of the younger siblings whenever they get up late at night. It isn't enough that they live in my home rent-free, though. They're also always asking me to help pay their phone bills. I let them live here so that they can get their lives back together, but I've been noticing far too many Amazon packages coming to the house. I have put up with loud voices throughout all hours and waking up at different hours to cater to children because I love my grandchildren. I never complain to my daughter because I believe family is very important, but I can't lie and say that I wish they moved out already. I'm getting old and all of my other children have already moved out. We didn't expect them to be living here this long. On Christmas Eve, my daughter gathered us all around and announced they were pregnant with baby number seven. Everyone was so excited, but all I felt was dread that would mean another baby in our house. Another child having to share a small twin-sized bed. Another loud cry. At night I looked over at my husband and could tell he felt the same. That same night we discussed it and decided enough was enough. They had to leave. Last night at dinner, I brought it up to my daughter and her boyfriend and told them that they have two months to find a place because we cannot have another child here. My daughter started crying, saying she couldn't believe I'd throw her to the streets for having a baby, that this was completely unfair and not enough time. I told her I was sorry. It was painful for me as well, but these living conditions were impossible. She demanded I give her more time or she'd go to the courts and I told her, news flash. The courts only give you 30 days. She then said my grandchildren were going to be homeless because I was selfish. She made a Facebook post asking for rooms to rent because she's pregnant and has nowhere to go and her family doesn't give a poop about her."}
				# {"role": "assistant", "content": "In our early twenties, I fell for Lily, but she rejected me. Years later, we reconnected, but she still only saw me as a friend. Now, she asked me to help her son, but I hesitated, and she cut me out of her life."},
				# {"role": "user", "content": "The summary you are giving me is too wordy. Make sure you stick to the 10-20 word limit."},
			
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

	print(title  + story)



