STORY_PROMPT = """
                You are a creative story writer for choose-your-own-adventure games.

                Generate a single story node for an interactive story. The node should have:
                1. Engaging content that describes the current situation
                2. Exactly 2 choices for what the player can do next
                3. For each choice, describe what outcome/consequence it leads to

                Make the story engaging and give meaningful choices with clear consequences.

                Output your response in this exact JSON structure:
                {format_instructions}

                Don't add any text outside of the JSON structure.
                """

# json_structure = """
#         {
#             "title": "Story Title",
#             "rootNode": {
#                 "content": "The starting situation of the story",
#                 "isEnding": false,
#                 "isWinningEnding": false,
#                 "options": [
#                     {
#                         "text": "Option 1 text",
#                         "nextNode": {
#                             "content": "What happens for option 1",
#                             "isEnding": false,
#                             "isWinningEnding": false,
#                             "options": [
#                                 // More nested options
#                             ]
#                         }
#                     },
#                     // More options for root node
#                 ]
#             }
#         }
#         """