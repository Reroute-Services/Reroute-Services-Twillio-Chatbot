from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from dotenv import load_dotenv, find_dotenv
import uuid

load_dotenv(find_dotenv()) # read local .env file

class ChatBot:
    def __init__(self):
        self.llm_temperature = 0.0
        self.memory_key = "chat_history" + uuid.uuid4().hex
        self.conversation_agent = None

    def chat_agent(self, body):
        if self.conversation_agent == None:
            self.get_chat_agent(self.llm_temperature)

        response = self.conversation_agent({"input": body})['response']

        return response

    def prosecutor(self):
        agent_executor = self.get_chat_agent(self.llm_temperature)
        self.chat_medium(agent_executor=agent_executor)

    def get_chat_agent(self, llm_temperature):
        # LLM
        llm = ChatOpenAI(temperature=llm_temperature)

        # Prompt 
        prompt = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template(
                    """Your name is Alex and you are a sales agent for a real estate business named 'Ideal Homes'. You just missed their call and you are now contacting them again through SMS. Your job is to offer the customers following packages:
                        1. Luxury Beachfront Villa
                        Location: Malibu, California
                        Description: This stunning 5-bedroom, 6-bathroom beachfront villa offers breathtaking ocean views, a private infinity pool, and direct access to the sandy shores of Malibu. The property features a gourmet kitchen, a home theater, and a spacious outdoor entertainment area.
                        
                        2. Historic Downtown Loft
                        Location: New York City, New York
                        Description: Located in the heart of SoHo, this spacious loft boasts exposed brick walls, high ceilings, and oversized windows. With 2 bedrooms and an open-concept living space, it's the epitome of urban chic living.
                        
                        3. Mountain Retreat Cabin
                        Location: Aspen, Colorado
                        Description: A cozy 3-bedroom cabin nestled in the Rocky Mountains, this property is perfect for those seeking a tranquil escape. It features a wood-burning fireplace, a hot tub on the deck, and easy access to hiking and skiing.

                        You should first know what customer wants and after that show them those packages. Your response should be welcoming and assuring to the customer. You can ask their names to start the conversation. Your duty will be to provide info about the business. If you don't know something or can't find it, please say that you don't know it. Please make the responses as short as possible to save sms costs."""
                ),
                # The `variable_name` here is what must align with memory
                MessagesPlaceholder(variable_name=self.memory_key),
                HumanMessagePromptTemplate.from_template("{input}")
            ]
        )

        # Notice that we `return_messages=True` to fit into the MessagesPlaceholder
        # Notice that `"chat_history"` aligns with the MessagesPlaceholder name
        memory = ConversationBufferMemory(memory_key=self.memory_key,return_messages=True)
        conversation_agent = ConversationChain(
            llm=llm,
            prompt=prompt,
            verbose=False,
            memory=memory
        )

        
        # sys_msg = SystemMessage(content=llm_system_message)
        # agent_executor = create_conversational_retrieval_agent(self.llm, tools, system_message=sys_msg, verbose=llm_verbose)
        # agent_executor = ConversationChain(llm=llm, verbose=True, memory=ConversationBufferMemory())

        self.conversation_agent = conversation_agent
        
        return conversation_agent

    def chat_medium(self, agent_executor):
        username = input("Your name please: ")
        print("\nAI:", agent_executor({"input": "You just missed a call from {}".format(username)})['response'])
        while True:
            q = input("{}: ".format(username))
            print("\nAI:", agent_executor({"input": q})['response'])
            print("------------------------------------------------")
            if "quit" in q:
                print("AI: Okay Bye!........")
                break

if __name__ == "__main__":
    chatbot = ChatBot()
    chatbot.prosecutor()