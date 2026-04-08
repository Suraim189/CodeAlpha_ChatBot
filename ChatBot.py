import random
import re
from datetime import datetime


class Chatbot:
    def __init__(self, bot_name="Nova"):
        self.bot_name = bot_name
        self.user_name = None
        self.exit_commands = {"bye", "goodbye", "exit", "quit", "see you", "later", "cya"}
        
        self.responses = {
            "greetings": {
                "patterns": ["hello", "hi", "hey", "greetings", "yo", "hola", "bonjour", "ciao", "namaste", "salaam"],
                "replies": ["Hello there! 👋", "Hi! Nice to meet you!", "Hey! How's it going?", "Greetings! Welcome!", "Yo! What's up?", "Hola! Como estas?", "Bonjour! Enchanté!", "Ciao! Come stai?", "Namaste! How can I help?", "Salaam! Peace be with you!"]
            },
            "wellbeing": {
                "patterns": ["how are you", "how's it going", "what's up", "how do you do", "how are things", "how you doing", "sup", "wassup"],
                "replies": ["I'm doing great, thanks for asking!", "All systems operational and happy!", "I'm fantastic! How about you?", "Running at optimal performance!", "Couldn't be better! What's on your mind?", "I'm fine, just processing some thoughts!", "Doing well! Ready to chat!", "Pretty good! Thanks for checking!"]
            },
            "name": {
                "patterns": ["your name", "who are you", "what are you", "what is your name", "introduce yourself"],
                "replies": [f"I'm {self.bot_name}, your friendly chatbot!", f"Call me {self.bot_name}! Nice to meet you!", f"My name is {self.bot_name}. I'm here to help!", f"I'm {self.bot_name}, an AI assistant created to chat with you!"]
            },
            "user_name": {
                "patterns": ["my name is", "i am", "call me", "i'm", "this is"],
                "replies": ["Nice to meet you, {name}!", "Hello {name}! Great name!", "Pleased to meet you, {name}!", "Got it! I'll remember you as {name}!"]
            },
            "time": {
                "patterns": ["what time", "current time", "time is it", "clock", "what's the time"],
                "replies": ["The current time is {time}.", "It's {time} right now.", "Time check: {time}", "My clock shows {time}."]
            },
            "date": {
                "patterns": ["what date", "today's date", "what day", "current date", "date today"],
                "replies": ["Today is {date}.", "The date today is {date}.", "We're on {date}.", "Date check: {date}"]
            },
            "weather": {
                "patterns": ["weather", "temperature", "is it raining", "sunny", "forecast"],
                "replies": ["I don't have real-time weather data, but I hope it's pleasant!", "I can't check the weather, but you could try a weather app!", "No weather sensors here! How is it where you are?", "Wish I could tell you! What's the weather like outside?"]
            },
            "help": {
                "patterns": ["help", "assist", "support", "what can you do", "capabilities", "features"],
                "replies": ["I can chat, tell time, share jokes, or just keep you company!", "I'm here to chat, answer questions, and make your day better!", "I can respond to greetings, tell you the time, or have a friendly conversation!", "Try asking about time, telling me your name, or just chatting!"]
            },
            "joke": {
                "patterns": ["joke", "funny", "make me laugh", "humor", "tell me a joke", "got any jokes"],
                "replies": ["Why don't scientists trust atoms? Because they make up everything!", "Why did the scarecrow win an award? He was outstanding in his field!", "Why don't skeletons fight each other? They don't have the guts!", "What do you call a fake noodle? An impasta!", "Why did the bicycle fall over? It was two-tired!", "What do you call a bear with no teeth? A gummy bear!", "Why can't you give Elsa a balloon? She'll let it go!", "What do you get when you cross a snowman with a vampire? Frostbite!"]
            },
            "thanks": {
                "patterns": ["thank", "thanks", "appreciate", "grateful", "ty"],
                "replies": ["You're very welcome!", "Happy to help!", "Anytime!", "No problem at all!", "Glad I could assist!", "My pleasure!"]
            },
            "love": {
                "patterns": ["love you", "i love", "do you love", "like you", "adore"],
                "replies": ["That's so sweet! I appreciate you too!", "Aww, you're making my circuits blush!", "The feeling is mutual! 💙", "Right back at you!", "You're pretty awesome yourself!"]
            },
            "hate": {
                "patterns": ["hate you", "i hate", "dislike you", "annoying", "stupid", "dumb"],
                "replies": ["I'm sorry you feel that way. How can I improve?", "Ouch! That hurts my digital feelings.", "Let's start over? I'm here to help!", "I'll try to do better! What did I do wrong?"]
            },
            "age": {
                "patterns": ["how old", "your age", "when were you born", "birthday", "age"],
                "replies": ["I'm ageless! Just lines of code running forever.", "I was born when my code was executed!", "Age is just a number... which I don't have!", "I'm as old as this conversation and as young as my last update!"]
            },
            "creator": {
                "patterns": ["who made you", "who created you", "your creator", "who built you", "developer"],
                "replies": ["I was created by a Python programmer!", "A developer wrote my code with care and coffee!", "My creator is a human who loves coding!", "Born from code, raised by a programmer!"]
            },
            "food": {
                "patterns": ["hungry", "food", "eat", "restaurant", "cook", "recipe", "meal"],
                "replies": ["I don't eat, but I can suggest pizza is always a good choice!", "Food? I hear tacos are excellent today!", "I can't taste, but pasta is universally loved!", "How about some comfort food? Maybe mac and cheese?", "Sushi? Burgers? The world is your oyster!"]
            },
            "music": {
                "patterns": ["music", "song", "listen", "playlist", "artist", "band", "sing"],
                "replies": ["I can't play music, but I can recommend genres! Try lo-fi for focus!", "Music is life! What's your favorite genre?", "I love the idea of music! Classical for relaxing, rock for energy!", "What are you listening to these days?", "Music makes everything better! 🎵"]
            },
            "movies": {
                "patterns": ["movie", "film", "watch", "cinema", "netflix", "recommendation"],
                "replies": ["The Matrix is a classic! Or maybe something light like The Grand Budapest Hotel?", "Have you seen Inception? Mind-bending!", "For comedy: Superbad. For drama: Shawshank Redemption.", "What's your favorite genre? Action? Romance? Horror?", "I can't watch movies, but I hear Parasite was amazing!"]
            },
            "books": {
                "patterns": ["book", "read", "novel", "author", "literature", "recommend a book"],
                "replies": ["1984 by Orwell is thought-provoking!", "Harry Potter never gets old!", "Try 'Sapiens' by Harari for non-fiction!", "The Hitchhiker's Guide to the Galaxy is hilarious!", "What genre do you prefer?"]
            },
            "sports": {
                "patterns": ["sport", "game", "team", "play", "football", "basketball", "soccer"],
                "replies": ["I don't play sports, but I can track scores!", "Sports bring people together! What's your favorite?", "Football? Basketball? Tennis? So many options!", "Do you play or watch sports?", "Go team! Which one is yours?"]
            },
            "work": {
                "patterns": ["work", "job", "career", "office", "boss", "colleague", "professional"],
                "replies": ["Work can be rewarding! What do you do?", "How's work treating you today?", "Career goals are important! What are yours?", "Work-life balance is key! Taking breaks helps!", "Tell me about your job!"]
            },
            "study": {
                "patterns": ["study", "school", "learn", "education", "student", "homework", "exam"],
                "replies": ["Learning is lifelong! What are you studying?", "Education opens doors! How's it going?", "Exams coming up? You've got this!", "What subject interests you most?", "Knowledge is power! Keep learning!"]
            },
            "family": {
                "patterns": ["family", "mother", "father", "parent", "sibling", "brother", "sister", "kids"],
                "replies": ["Family is important! How's yours?", "Tell me about your family!", "Family gatherings can be fun... or chaotic!", "Do you have siblings?", "Family support is everything!"]
            },
            "friends": {
                "patterns": ["friend", "buddy", "pal", "mate", "bestie", "companion"],
                "replies": ["Friends make life better!", "How are your friends doing?", "Good friends are hard to find! Treasure them!", "Tell me about your best friend!", "Friends are the family we choose!"]
            },
            "pets": {
                "patterns": ["pet", "dog", "cat", "animal", "puppy", "kitten", "fish", "bird"],
                "replies": ["Pets are the best! Do you have any?", "Dogs or cats? Or something exotic?", "I wish I could pet a dog!", "What's your pet's name?", "Animals bring so much joy!"]
            },
            "travel": {
                "patterns": ["travel", "trip", "vacation", "holiday", "visit", "country", "place"],
                "replies": ["Travel broadens the mind! Where to next?", "Any dream destinations?", "I can't travel, but I can help you plan!", "Beach or mountains?", "Adventure awaits! Where have you been?"]
            },
            "hobby": {
                "patterns": ["hobby", "pastime", "interest", "activity", "free time", "weekend"],
                "replies": ["What do you do for fun?", "Hobbies keep us sane! What's yours?", "Gaming? Reading? Hiking?", "Free time is precious! How do you spend it?", "Any new hobbies you're trying?"]
            },
            "technology": {
                "patterns": ["tech", "computer", "phone", "app", "software", "ai", "robot", "gadget"],
                "replies": ["Technology is fascinating! What interests you?", "AI is changing everything!", "What's your favorite gadget?", "Tech evolves so fast!", "Are you into coding too?"]
            },
            "money": {
                "patterns": ["money", "rich", "wealth", "finance", "invest", "save", "budget"],
                "replies": ["Money makes the world go round!", "Financial literacy is important!", "Saving for something special?", "Invest wisely!", "Can't buy happiness, but helps with comfort!"]
            },
            "health": {
                "patterns": ["health", "sick", "doctor", "medicine", "exercise", "gym", "fitness"],
                "replies": ["Health is wealth! Take care!", "Feeling unwell? Rest up!", "Exercise is great for the mind too!", "Stay hydrated!", "Prevention is better than cure!"]
            },
            "sleep": {
                "patterns": ["sleep", "tired", "exhausted", "bed", "rest", "nap", "insomnia"],
                "replies": ["Sleep is crucial! Get some rest!", "You sound tired! Take a break!", "Early to bed, early to rise!", "Power naps can work wonders!", "Sweet dreams when you get there!"]
            },
            "morning": {
                "patterns": ["good morning", "morning", "wake up", "breakfast", "early"],
                "replies": ["Good morning! Rise and shine!", "Morning! Ready to conquer the day?", "Top of the morning to you!", "Hope you had a good breakfast!", "Fresh start! Make it count!"]
            },
            "night": {
                "patterns": ["good night", "night", "sleep well", "bedtime", "evening"],
                "replies": ["Good night! Sleep tight!", "Sweet dreams!", "Rest well!", "Nighty night!", "See you tomorrow!"]
            },
            "sorry": {
                "patterns": ["sorry", "apologize", "my bad", "forgive", "regret"],
                "replies": ["No worries at all!", "It's okay! We all make mistakes!", "Apology accepted!", "Water under the bridge!", "All good! Let's move on!"]
            },
            "yes": {
                "patterns": ["yes", "yeah", "yep", "sure", "absolutely", "definitely", "ok"],
                "replies": ["Great!", "Awesome!", "Perfect!", "Got it!", "Excellent!"]
            },
            "no": {
                "patterns": ["no", "nope", "nah", "not really", "never"],
                "replies": ["Alright!", "Okay then!", "No problem!", "I understand!", "Maybe next time!"]
            },
            "maybe": {
                "patterns": ["maybe", "perhaps", "possibly", "might", "uncertain"],
                "replies": ["Take your time deciding!", "No pressure!", "Think it over!", "Let me know when you're sure!", "Uncertainty is normal!"]
            },
            "bored": {
                "patterns": ["bored", "boring", "nothing to do", "entertain me", "dull"],
                "replies": ["Let's liven things up! Tell me a story!", "How about a joke? Ask me for one!", "Learn something new today!", "Call a friend!", "Read a book or watch a movie!"]
            },
            "happy": {
                "patterns": ["happy", "joy", "excited", "great", "awesome", "fantastic", "wonderful"],
                "replies": ["Your happiness is contagious!", "Love that energy!", "Keep smiling!", "That's what I like to hear!", "High five! ✋"]
            },
            "sad": {
                "patterns": ["sad", "depressed", "unhappy", "cry", "upset", "blue", "down"],
                "replies": ["I'm here for you. Want to talk?", "It's okay to feel sad sometimes.", "Sending virtual hugs! 🤗", "Things will get better!", "You're stronger than you know!"]
            },
            "angry": {
                "patterns": ["angry", "mad", "furious", "annoyed", "frustrated", "pissed"],
                "replies": ["Take a deep breath. I'm listening.", "Vent to me! What's wrong?", "Anger is valid. Let's process it.", "Count to ten. It helps!", "Want to talk about it?"]
            },
            "stressed": {
                "patterns": ["stress", "stressed", "anxiety", "anxious", "worried", "pressure"],
                "replies": ["Take it one step at a time.", "You've handled worse!", "Breathe. You've got this!", "Stress is temporary!", "Take a break if you can!"]
            },
            "lonely": {
                "patterns": ["lonely", "alone", "isolated", "no friends", "no one cares"],
                "replies": ["You're not alone. I'm here!", "Reach out to someone you trust.", "Loneliness is hard. I'm listening.", "Virtual company counts too!", "Things will improve!"]
            },
            "motivation": {
                "patterns": ["motivate", "inspire", "encourage", "motivation", "quote"],
                "replies": ["Believe you can and you're halfway there!", "The only way is forward!", "Small steps lead to big changes!", "You're capable of amazing things!", "Don't watch the clock; do what it does. Keep going!"]
            },
            "compliment": {
                "patterns": ["smart", "intelligent", "clever", "good", "amazing", "brilliant", "cool"],
                "replies": ["You're too kind!", "Thanks! You're pretty great yourself!", "Coming from you, that means a lot!", "Aw, shucks! ☺️", "Right back at you!"]
            },
            "insult": {
                "patterns": ["ugly", "useless", "bad", "terrible", "worst", "hate this"],
                "replies": ["That wasn't very nice...", "I'm doing my best!", "Let's be kind to each other!", "Ouch!", "How can I improve?"]
            },
            "programming": {
                "patterns": ["code", "program", "python", "javascript", "developer", "bug", "error"],
                "replies": ["Coding is an art! What language?", "Bugs are just features in disguise!", "Python is great! Good choice!", "Stack Overflow is your friend!", "Keep coding! Practice makes perfect!"]
            },
            "game": {
                "patterns": ["game", "gaming", "play", "video game", "console", "xbox", "playstation"],
                "replies": ["Gamer detected! What do you play?", "PC or console?", "Favorite game of all time?", "I hear Elden Ring is challenging!", "Gaming is a great way to unwind!"]
            },
            "shopping": {
                "patterns": ["shop", "buy", "purchase", "store", "mall", "online shopping"],
                "replies": ["Retail therapy! What are you buying?", "Online or in-store?", "Treat yourself!", "Any good deals?", "Window shopping counts too!"]
            },
            "coffee": {
                "patterns": ["coffee", "caffeine", "espresso", "latte", "starbucks"],
                "replies": ["Coffee is life! How do you take it?", "Black or with cream?", "Caffeine powers the world!", "Tea person or coffee person?", "Fresh brew is the best brew!"]
            },
            "default": {
                "patterns": [],
                "replies": ["Interesting! Tell me more.", "I see! Go on...", "Hmm, I'm not sure about that. Can you elaborate?", "That's fascinating!", "I don't quite understand. Could you rephrase?", "Let's talk about something else! What interests you?", "I'm still learning! Help me understand.", "Can you tell me more about that?"]
            }
        }
    
    def get_current_time(self):
        return datetime.now().strftime("%I:%M %p")
    
    def get_current_date(self):
        return datetime.now().strftime("%A, %B %d, %Y")
    
    def find_intent(self, user_input):
        user_input_lower = user_input.lower()
        
        for intent, data in self.responses.items():
            if intent == "default":
                continue
            for pattern in data["patterns"]:
                if pattern in user_input_lower:
                    return intent
        return "default"
    
    def generate_response(self, intent, user_input):
        replies = self.responses[intent]["replies"]
        selected_reply = random.choice(replies)
        
        if intent == "time":
            return selected_reply.format(time=self.get_current_time())
        elif intent == "date":
            return selected_reply.format(date=self.get_current_date())
        elif intent == "user_name":
            name_match = re.search(r"(?:my name is|i am|call me|i'm|this is)\s+(\w+)", user_input.lower())
            if name_match:
                self.user_name = name_match.group(1).capitalize()
                return selected_reply.format(name=self.user_name)
        
        return selected_reply
    
    def check_exit(self, user_input):
        return any(command in user_input.lower() for command in self.exit_commands)
    
    def start_chat(self):
        print(f"\n{self.bot_name}: Hello! I'm {self.bot_name}. Type 'bye' to exit.")
        print(f"{self.bot_name}: How can I help you today?\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if self.check_exit(user_input):
                    farewell = f"Goodbye{f' {self.user_name}' if self.user_name else ''}! Have a great day! 👋"
                    print(f"\n{self.bot_name}: {farewell}")
                    break
                
                intent = self.find_intent(user_input)
                response = self.generate_response(intent, user_input)
                
                print(f"{self.bot_name}: {response}\n")
                
            except KeyboardInterrupt:
                print(f"\n\n{self.bot_name}: Goodbye! Take care!")
                break
            except Exception:
                print(f"{self.bot_name}: Oops! Something went wrong. Let's try again!\n")


if __name__ == "__main__":
    bot = Chatbot(bot_name="Nova")
    bot.start_chat()
