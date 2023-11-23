from abc import ABC
#위에가 파이썬에서 추상 클래스 만드는 방법

#추상화 -> 인간, 뭐 그런 것들(추상클래스를 반드시 만들어야 함)
class Predictor(ABC):
    @abstractmethod
    def load_model(model_path: str):
        pass
    
    @abstractmethod
    def predict(input):
        pass