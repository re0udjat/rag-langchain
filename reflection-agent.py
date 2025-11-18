import os
from dotenv import load_dotenv
from typing import Annotated, TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import (
  AIMessage,
  BaseMessage,
  HumanMessage,
  SystemMessage
)
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages

# Load environment variables from .env file
load_dotenv()

# Define model
model = ChatOpenAI(
  base_url=os.getenv("OPENAI_API_URL"),
  api_key=os.getenv("OPENAI_API_KEY"),
  model=os.getenv("OPENAI_API_MODEL"),
  temperature=0.5,
)

# Define prompt
generate_prompt = SystemMessage(
  """Bạn là trợ lý viết luận được giao nhiệm vụ viết bài luận 3 đoạn văn 
    xuất sắc"""
  """Tạo ra bài luận tốt nhất theo yêu cầu của người dùng."""
  """Nếu người dùng đưa ra lời phê bình, hãy phản hồi bằng phiên bản sửa đổi 
    của những lần thử trước đó."""
)

reflection_prompt = SystemMessage(
  """Bạn là giáo viên đang chấm bài luận. Hãy tạo bài phê bình và khuyến nghị
    cho bài luận của người dùng."""
  """Đưa ra các khuyến nghị chi tiết, bao gồm yêu cầu về độ dài, độ sâu, phong
    cách, v.v...
  """
  """Bạn cần phê bình và khuyến nghị cho bài luận bằng ngôn ngữ Việt Nam.
  """
)

# Define Graph
class State(TypedDict):
  messages: Annotated[list[BaseMessage], add_messages]

def generate(state: State) -> State:
  answer = model.invoke([generate_prompt] + state["messages"])
  return {
    "messages": answer
  }

def reflect(state: State) -> State:
  # Invert the messages to get the LLM to reflect on its own output
  cls_map = {
    AIMessage: HumanMessage,
    HumanMessage: AIMessage
  }

  # First message is the original user request
  # Hold it for the same for all nodes
  translated = [reflection_prompt, state["messages"][0]] + [
    cls_map[msg.__class__](content=msg.content) for msg in state["messages"][1:]
  ]
  answer = model.invoke(translated)

  # Treat the output of this as human feedback for the generator
  return {
    "messages": [HumanMessage(content=answer.content)]
  }

def should_continue(state: State):
  # End after 3 iterations, each with 2 messages
  if len(state["messages"]) > 6:
    return END
  else:
    return "reflect"
  
builder = StateGraph(State)
builder.add_node("generate", generate)
builder.add_node("reflect", reflect)
builder.add_edge(START, "generate")
builder.add_edge("reflect", "generate")
builder.add_conditional_edges("generate", should_continue)
graph = builder.compile()

# Run app
def main():
  input = {
    "messages": [
      HumanMessage("""Bài luận của bạn về tính thời sự của "Hoàng tử bé" và
    thông điệp của nó trong cuộc sống hiện đại được viết rất hay và sâu
    sắc. Bạn đã làm nổi bật một cách hiệu quả tính liên quan lâu dài của
    các chủ đề trong cuốn sách và tầm quan trọng của nó trong xã hội ngày
    nay. Tuy nhiên, có một vài điểm bạn có thể cải thiện bài luận của mình:
    
    1. **Chiều sâu**: Khi bạn đề cập đến các chủ đề về việc trân trọng những
    niềm vui giản dị, nuôi dưỡng các mối quan hệ và thấu hiểu các mối quan
    hệ giữa người với người, hãy cân nhắc đào sâu hơn vào từng chủ đề này.
    Hãy đưa ra các ví dụ cụ thể từ cuốn sách để hỗ trợ luận điểm của bạn và
    khám phá cách những chủ đề này thể hiện trong cuộc sống đương đại.

    2. **Phân tích**: Hãy cân nhắc việc phân tích xem thông điệp của cuốn sách
    có thể được áp dụng như thế nào trong các vấn đề xã hội hiện tại hoặc trải
    nghiệm cá nhân. Ví dụ, bạn có thể thảo luận về mối liên hệ giữa quan điểm
    của Hoàng tử bé về chủ nghĩa vật chất với văn hóa tiêu dùng hoặc khám phá
    cách tiếp cận của anh ấy đối với các mối quan hệ có thể ảnh hưởng đến các
    động lực giao tiếp giữa các cá nhân trong thời đại kỹ thuật số.

    3. **Độ dài**: Mở rộng ý tưởng của bạn bằng cách thêm ví dụ, thảo luận các phản
    biện, hoặc khám phá tác động văn hóa của "Hoảng tử bé" ở các khu vực khác nhau
    trên thế giới. Điều này sẽ làm phong phú thêm chiều sâu cho bài phân tích của
    bạn và cung cấp hiểu biết toàn diện hơn về tính liên quan của cuốn sách.

    4. **Phong cách**: Bài luận của bạn rõ ràng và có cấu trúc tốt. Để tăng sự thu
    hút của người đọc, hãy cân nhắc việc trích dẫn từ sách để minh họa các điểm chính
    hoặc thêm vào các giai thoại để cá nhân hóa bài phân tích của bạn. 

    5. **Kết luận**: Kết thúc bài luận bằng cách tóm tắt ý nghĩa lâu dài của "Hoàng
    tử bé" và cách những thông điệp của nó có thể truyền cảm hứng cho những thay đổi
    tích cực trong xã hội hiện đại. Hãy suy ngẫm về những hàm ý rộng hơn trong sách và
    để lại cho người đọc ấn tượng sâu sắc.
                   
    6. **Ngôn ngữ**: Bắt buộc bài luận của bạn phải viết bằng ngôn ngữ Việt Nam mà
    không được phép có bất kỳ ngôn ngữ nào khác như ngôn ngữ Anh, ngôn ngữ Trung 
    Quốc, v.v...

    Bằng cách mở rộng phân tích, đưa thêm ví dụ và đào sâu việc khám phá thông điệp
    của cuốn sách, bạn có thể tạo nên một bài luận toàn diện và hấp dẫn hơn về tính
    thời sự của "Hoàng tử bé" trong cuộc sống hiện đại. Chúc mừng bạn đã phân tích
    chu đáo, và hãy tiếp tục phát huy nhé!
    """)
    ]
  }
  for chunk in graph.stream(input):
    if "generate" in chunk:
        print("AI GENERATE PROMPT:")
        print(chunk["generate"]["messages"].content)
        print("\n\n\n")
    elif "reflect" in chunk:
        print("AI REFLECTION PROMPT:")
        for idx in range(len(chunk)):
            print(chunk["reflect"]["messages"][idx].content, end="\n\n\n")
        print("\n\n\n")

main()