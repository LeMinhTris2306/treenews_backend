from typing import Optional, List
from pydantic import ConfigDict, BaseModel, Field, model_validator
from bson import ObjectId
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
import json

PyObjectId = Annotated[str, BeforeValidator(str)]

class ImageModel(BaseModel):
    imgTitle: str = Field(...)
    imgName: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "imgTitle": "Mbappe có một đêm đáng quên khác trong màu áo Real Madrid. Ảnh: EFE",
                "imgName": "yourimgname.jpg"
            }
        },
    )

class ContextModel(BaseModel):
    context: str = Field(...)
    img: Optional[ImageModel] = Field(None, description="Thông tin hình ảnh đi kèm, có thể không có.")
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "context": "Anh ấy toát ra sự lo lắng. Mbappe thậm chí không còn là một cầu thủ bóng đá nữa.",
                "img": {
                    "imgTitle": "Mbappe có một đêm đáng quên khác trong màu áo Real Madrid. Ảnh: EFE",
                    "imgName": "yourimgname.jpg"
                }
            }
        },
    )

class ArticleModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str = Field(...)
    uploadDay: str = Field(...)
    detail: List[ContextModel] = Field(...)
    displayName: str = Field(...)
    authorId: str = Field(...)
    categoryId: str = Field(...)
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "title": "HLV Kim Sang Sik: ĐT Việt Nam giờ không còn sợ Thái Lan",
                "uploadDay": "01/01/2025",
                "detail": [
                    {
                        "context": """HLV Kim Sang Sik của ĐT Việt Nam có những phát biểu đáng chú ý trước trận chung kết lượt đi AFF Cup 2024 với Thái Lan.
Tối 2/1, ĐT Việt Nam sẽ tiếp đón Thái Lan ở trận chung kết lượt đi AFF Cup 2024 trên SVĐ Việt Trì (Phú Thọ). Đây là màn đọ sức tái hiện trận tranh ngôi vô địch ở kỳ gần nhất năm 2022.
Khi ấy, ĐT Việt Nam dưới sự dẫn dắt của HLV Park Hang Seo đã để thua tổng tỷ số 2-3 qua đó nhìn đại kình địch lên ngôi vương. Lần này, cũng với một thuyền trưởng người Hàn Quốc - HLV Kim Sang Sik, "Những chiến binh Sao Vàng" kỳ vọng sẽ biến chuyển tích cực.
Chia sẻ ở buổi họp báo trước trận, HLV Kim Sang Sik mở đầu: "Chúc mừng năm mới tất cả mọi người. Thái Lan là một ngọn núi lớn, tuy nhiên không có ngọn núi nào không thể vượt qua. Tôi hy vọng ngày mai sẽ đưa ĐT Việt Nam lên đỉnh núi, mong rằng các cầu thủ sẽ thể hiện được tốt nhất".""",
                        "img": {
                            "imgTitle": "HLV Kim Sang Sik trả lời họp báo trước trận chung kết gặp Thái Lan (Ảnh: VFF)",
                            "imgName": "yourimgname.jpg"
                        }
                    }
                    #,
#                     {
#                         "context": """Tôi biết đến thông tin trận đấu giữa ĐT Việt Nam và Thái Lan được xem là "derby Đông Nam Á", cũng như tôi là người Hàn Quốc và HLV trưởng của ĐT Thái Lan là người Nhật Bản. Trận ngày mai sẽ rất khó khăn, nhưng ĐT Việt Nam đã thắng Singapore (dẫn dắt bởi HLV người Nhật Bản) ở bán kết, từ cơ sở đó tôi hy vọng có một trận đấu tốt trước HLV người Nhật Bản của Thái Lan", HLV Kim Sang Sik nói thêm
# HLV Kim Sang Sik nhận xét về đối thủ: "Thái Lan đã có một trận đấu vất vả, trải qua 120 phút trước Philippines. Tôi biết họ đang vất vả và mệt mỏi về thể lực. Tôi nghĩ đây cũng là điều mà chúng tôi cần tập trung để tận dụng, tấn công. Chúng tôi sẽ cố gắng thi đấu theo kế hoạch đã định ra.
# Nếu chúng tôi không ngừng nỗ lực, tôi tin cơ hội (ghi bàn) sẽ đến với chúng tôi. Cùng với đó, trận đấu ngày mai chúng tôi được thi đấu trên sân nhà, với sự cổ vũ nhiệt thành, các cầu thủ không chùn bước, quyết tâm để có một trận đấu tốt".
# Chiến lược gia người Hàn Quốc cho biết các học trò của ông giờ không sợ người Thái. "Tôi muốn nhấn mạnh rằng việc cầu thủ Việt Nam luôn có tâm lý yếu trước Thái Lan là chuyện của quá khứ
# ĐT Việt Nam giờ chỉ tập trung vào hiện tại. Các học trò của tôi hiện có tâm lý tốt hơn bao giờ hết. Tôi nói với họ thông điệp rằng một là vô địch, hai cũng phải là vô địch chứ không có kết quả nào khác".""",
#                         "img": {
#                             "imgTitle": "HLV Kim Sang Sik cho rằng ĐT Việt Nam giờ không còn sợ Thái Lan",
#                             "imgName": "yourimgname.jpg"
#                         }
#                     },
#                     {
#                         "context": """Nói về việc lựa chọn thủ môn bắt chính cho ĐT Việt Nam ở trận chung kết AFF Cup 2024, HLV Kim Sang Sik hé lộ: "26 cầu thủ Việt Nam đều sẵn sàng ra sân trong các trận đấu của giải. Tôi nói với cả Đình Triệu và Filip rằng cả hai đều là những thủ môn giỏi
# Tuy nhiên tùy từng trận đấu, tôi sẽ chỉ có một lựa chọn phù hợp với hệ thống. Đình Triệu có lợi thế hơn khi là người Việt Nam 100% nên có khả năng giao tiếp, kết nối tốt hơn tới các đồng đội"
# Ở lần gặp nhau gần nhất hồi tháng 9, Thái Lan ngược dòng thắng ĐT Việt Nam 2-1 trong trận giao hữu FIFA Days. Trong 90 phút tại Mỹ Đình, Nguyễn Tiến Linh mở tỷ số, nhưng lần lượt Mueanta và Patrik Gustavsson đưa Thái Lan vượt lên ngay trong hiệp một
# Tại đấu trường AFF Cup, Việt Nam thua 0-2 và hòa 0-0 ở bán kết 2020, rồi hòa 2-2 và thua 0-1 ở chung kết 2022, trước khi thua tiếp ở giao hữu năm nay."""
#                     }
                ],
                "displayName": "hlv-kim-sang-sik-noi-cung-truoc-chung-ket-aff-cup-voi-thai-lan",
                "authorId": "674869091328903d9b56a0a9",
                "categoryId": "6748701d1328903d9b56a0bb"
            }
        },
    )
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
    
class UpdateArticleModel(BaseModel):
    title: Optional[str] = None
    uploadDay: Optional[str] = None
    detail: Optional[List[ContextModel]] = None
    displayName: Optional[str] = None
    authorId: Optional[str] = None
    categoryId: Optional[str] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "title": "HLV Kim Sang Sik: ĐT Việt Nam giờ không còn sợ Thái Lan",
                "uploadDay": "31/12/2024",
                "detail": [
                    {
                        "context": """
                        HLV Kim Sang Sik của ĐT Việt Nam có những phát biểu đáng chú ý trước trận chung kết lượt đi AFF Cup 2024 với Thái Lan.
                        Tối 2/1, ĐT Việt Nam sẽ tiếp đón Thái Lan ở trận chung kết lượt đi AFF Cup 2024 trên SVĐ Việt Trì (Phú Thọ). Đây là màn đọ sức tái hiện trận tranh ngôi vô địch ở kỳ gần nhất năm 2022.
                        Khi ấy, ĐT Việt Nam dưới sự dẫn dắt của HLV Park Hang Seo đã để thua tổng tỷ số 2-3 qua đó nhìn đại kình địch lên ngôi vương. Lần này, cũng với một thuyền trưởng người Hàn Quốc - HLV Kim Sang Sik, "Những chiến binh Sao Vàng" kỳ vọng sẽ biến chuyển tích cực.
                        Chia sẻ ở buổi họp báo trước trận, HLV Kim Sang Sik mở đầu: "Chúc mừng năm mới tất cả mọi người. Thái Lan là một ngọn núi lớn, tuy nhiên không có ngọn núi nào không thể vượt qua. Tôi hy vọng ngày mai sẽ đưa ĐT Việt Nam lên đỉnh núi, mong rằng các cầu thủ sẽ thể hiện được tốt nhất".
                        """,
                        "img": {
                            "imgTitle": "HLV Kim Sang Sik trả lời họp báo trước trận chung kết gặp Thái Lan (Ảnh: VFF)",
                            "imgName": "path/to/your/img"
                        }
                    },
                    {
                        "context": """
                        "Tôi biết đến thông tin trận đấu giữa ĐT Việt Nam và Thái Lan được xem là 'derby Đông Nam Á', cũng như tôi là người Hàn Quốc và HLV trưởng của ĐT Thái Lan là người Nhật Bản. Trận ngày mai sẽ rất khó khăn, nhưng ĐT Việt Nam đã thắng Singapore (dẫn dắt bởi HLV người Nhật Bản) ở bán kết, từ cơ sở đó tôi hy vọng có một trận đấu tốt trước HLV người Nhật Bản của Thái Lan", HLV Kim Sang Sik nói thêm
                        HLV Kim Sang Sik nhận xét về đối thủ: "Thái Lan đã có một trận đấu vất vả, trải qua 120 phút trước Philippines. Tôi biết họ đang vất vả và mệt mỏi về thể lực. Tôi nghĩ đây cũng là điều mà chúng tôi cần tập trung để tận dụng, tấn công. Chúng tôi sẽ cố gắng thi đấu theo kế hoạch đã định ra.
                        Nếu chúng tôi không ngừng nỗ lực, tôi tin cơ hội (ghi bàn) sẽ đến với chúng tôi. Cùng với đó, trận đấu ngày mai chúng tôi được thi đấu trên sân nhà, với sự cổ vũ nhiệt thành, các cầu thủ không chùn bước, quyết tâm để có một trận đấu tốt".
                        Chiến lược gia người Hàn Quốc cho biết các học trò của ông giờ không sợ người Thái. "Tôi muốn nhấn mạnh rằng việc cầu thủ Việt Nam luôn có tâm lý yếu trước Thái Lan là chuyện của quá khứ
                        ĐT Việt Nam giờ chỉ tập trung vào hiện tại. Các học trò của tôi hiện có tâm lý tốt hơn bao giờ hết. Tôi nói với họ thông điệp rằng một là vô địch, hai cũng phải là vô địch chứ không có kết quả nào khác"
                        """,
                        "img": {
                            "imgTitle": "HLV Kim Sang Sik cho rằng ĐT Việt Nam giờ không còn sợ Thái Lan",
                            "imgName": "path/to/your/img"
                        }
                    },
                    {
                        "context": """
                            Nói về việc lựa chọn thủ môn bắt chính cho ĐT Việt Nam ở trận chung kết AFF Cup 2024, HLV Kim Sang Sik hé lộ: "26 cầu thủ Việt Nam đều sẵn sàng ra sân trong các trận đấu của giải. Tôi nói với cả Đình Triệu và Filip rằng cả hai đều là những thủ môn giỏi
                            Tuy nhiên tùy từng trận đấu, tôi sẽ chỉ có một lựa chọn phù hợp với hệ thống. Đình Triệu có lợi thế hơn khi là người Việt Nam 100% nên có khả năng giao tiếp, kết nối tốt hơn tới các đồng đội"
                            Ở lần gặp nhau gần nhất hồi tháng 9, Thái Lan ngược dòng thắng ĐT Việt Nam 2-1 trong trận giao hữu FIFA Days. Trong 90 phút tại Mỹ Đình, Nguyễn Tiến Linh mở tỷ số, nhưng lần lượt Mueanta và Patrik Gustavsson đưa Thái Lan vượt lên ngay trong hiệp một
                            Tại đấu trường AFF Cup, Việt Nam thua 0-2 và hòa 0-0 ở bán kết 2020, rồi hòa 2-2 và thua 0-1 ở chung kết 2022, trước khi thua tiếp ở giao hữu năm nay.
                        """
                    }
                ],
                "displayName": "hlv-kim-sang-sik-noi-cung-truoc-chung-ket-aff-cup-voi-thai-lan",
                "authorId": "674869091328903d9b56a0a9",
                "categoryId": "6748701d1328903d9b56a0bb"
            }
        },
    )
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

class ArticleCollection(BaseModel):
    articles: List[ArticleModel]