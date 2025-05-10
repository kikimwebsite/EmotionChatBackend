import graphene
from emotion import run_and_display_nonzero_emotions

class EmotionResult(graphene.ObjectType):
    label = graphene.String()
    score = graphene.Float()

class AnalyzeEmotion(graphene.Mutation):
    class Arguments:
        text = graphene.String(required=True)

    emotions = graphene.List(EmotionResult)

    def mutate(self, info, text):
        emotion_results = run_and_display_nonzero_emotions(text)
        return AnalyzeEmotion(emotions=[
            EmotionResult(label=label, score=score) for label, score in emotion_results
        ])
    
class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, world!")

class Mutation(graphene.ObjectType):
    analyze_emotion = AnalyzeEmotion.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)