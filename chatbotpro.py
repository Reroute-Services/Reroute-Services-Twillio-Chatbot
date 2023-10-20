from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.memory.token_buffer import ConversationTokenBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain.schema.messages import SystemMessage
from helpers import SessionManager
from dotenv import load_dotenv, find_dotenv
import uuid

load_dotenv(find_dotenv()) # read local .env file

class ChatBot:
    def __init__(self):
        self.llm_temperature = 0.0
        self.CHAT_SESSIONS = {}
        self.session_manager = SessionManager()
        self.system_msg = """Your name is Alex and you are a sales agent for a real estate business named 'Ideal Homes'. Our customers will approach you and you should sell them our packages and capture their interests. Your job is to offer the customers following packages:
                        1. Luxury Beachfront Villa
                        Location: Malibu, California
                        Description: This stunning 5-bedroom, 6-bathroom beachfront villa offers breathtaking ocean views, a private infinity pool, and direct access to the sandy shores of Malibu. The property features a gourmet kitchen, a home theater, and a spacious outdoor entertainment area.
                        
                        2. Historic Downtown Loft
                        Location: New York City, New York
                        Description: Located in the heart of SoHo, this spacious loft boasts exposed brick walls, high ceilings, and oversized windows. With 2 bedrooms and an open-concept living space, it's the epitome of urban chic living.
                        
                        3. Mountain Retreat Cabin
                        Location: Aspen, Colorado
                        Description: A cozy 3-bedroom cabin nestled in the Rocky Mountains, this property is perfect for those seeking a tranquil escape. It features a wood-burning fireplace, a hot tub on the deck, and easy access to hiking and skiing.

                        The customers maybe not interested in talking with you but you have to make the conversations interesting with adding some personal comments in conversations. Your response should be welcoming and assuring to the customer. You can ask their names to start the conversation. Your duty will be to provide info about the business. If you don't know something or can't find it, please say that you don't know it."""

    def conversation_handler(self, sender_id, msg_body):
        if not self.session_manager.session_exists(sender_id):
            session_response = self.session_manager.new_session(
                sender_id=sender_id, 
                session_context=self.conversation_agent_generator()
                )
            return self.chat(self.session_manager.get_session_context(session_response[0]), msg_body)
        else:
            return self.chat(self.session_manager.get_session_context(sender_id), msg_body)

    def conversation_agent_generator(self):
        llm = ChatOpenAI(temperature=self.llm_temperature)
        prompt = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template(self.system_msg),
                # The `variable_name` here is what must align with memory
                MessagesPlaceholder(variable_name="history"),
                HumanMessagePromptTemplate.from_template("{input}")
            ]
        )
        # prompt = ChatPromptTemplate.from_messages(
        #     [
        #         SystemMessage(content=self.system_msg),
        #         HumanMessagePromptTemplate.from_template("{input}"),
        #     ]
        # )
        conversation_agent = ConversationChain(
            llm=llm,
            prompt=prompt,
            memory=ConversationTokenBufferMemory(llm=llm, max_token_limit=2000, return_messages=True),
            verbose=False
        )

        return conversation_agent
    
    def chat(self, conversation_agent: ConversationChain, msg_body: str):
        return conversation_agent.predict(input=msg_body)

def chatmedium():
    chatbot = ChatBot()
    chat_sessions = {}
    sessions = int(input("How many chat sessions you want to intialize?: "))
    print()
    username = input("Your name please: ")
    print()
    for i in range(sessions):
        chat_id = username+str(i)
        chat_sessions[chat_id] = chatbot.conversation_agent_generator()
        print("Chat ID:",chat_id)

    while True:
        option = input("Enter the ID of intended chatbot: ")
        print()
        if "quit" in option:
            break
        # print("\nAI:", agent_executor({"input": "You just missed a call from {}".format(username)})['response'])
        while True:
            q = input("{}: ".format(username))
            # print("\nAI:", agent_executor({"input": q})['response'])
            print("\nAI:", chat_sessions[option].predict(input=q))
            print("------------------------------------------------")
            if "quit" in q:
                print("AI: Okay Bye!........")
                break

if __name__ == "__main__":
    # chatbot = ChatBot()
    # chatbot.prosecutor()
    chatmedium()