import os
import sys

a = int(input("Demo # : "))

if (a == 1):
    from chatbot import demo

    demo()
elif (a == 2 ):
    from chatbot import Chat, register_call
    import wikipedia
    import os
    import warnings
    warnings.filterwarnings("ignore")


    @register_call("whoIs")
    def who_is(session, query):
        try:
            return wikipedia.summary(query)
        except Exception:
            for new_query in wikipedia.search(query):
                try:
                    return wikipedia.summary(new_query)
                except Exception:
                    pass
        return "I don't know about "+query


    first_question = "Hi, how are you?"
    chat = Chat(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Example.template"))
    chat.converse(first_question)
else:
    print("\nInvalid Demo #\n")
    quit()