"""Build a deliberately small, authored teaching corpus. No customer/student data."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "week11/lab/data"
# These are fictional shop policies, not MUSINSA policies or legal advice.
POLICIES = [
    ("return", "반품 접수", "상품 수령 후 7일 이내 반품을 접수합니다. 착용 흔적과 택 제거가 없는 상품만 가능합니다."),
    ("return_cost", "반품 배송비", "단순 변심 반품 배송비는 3000원입니다. 상품 불량 또는 오배송의 반품 배송비는 판매자가 부담합니다."),
    ("exchange", "사이즈 교환", "사이즈 교환은 수령 후 7일 이내 신청합니다. 재고가 없으면 교환 대신 반품을 안내합니다."),
    ("exchange_cost", "교환 배송비", "단순 변심 사이즈 교환의 왕복 배송비는 6000원입니다. 불량 상품 교환은 무료입니다."),
    ("refund", "환불 소요 기간", "반품 검수가 완료된 후 영업일 기준 3일 이내 환불을 요청합니다. 카드사 반영일은 별도입니다."),
    ("cancel", "주문 취소", "결제 완료 상태에서는 주문 취소가 가능합니다. 출고 준비 이후에는 취소 대신 배송 완료 후 반품을 접수합니다."),
    ("delivery", "일반 배송", "일반 배송은 출고 후 영업일 기준 2일에서 4일이 걸립니다. 예약 상품은 상품 페이지의 출고 예정일을 따릅니다."),
    ("island", "제주 배송", "제주 지역은 기본 배송비 외에 3000원이 추가됩니다. 도서 산간 지역의 정확한 비용은 결제 화면에서 확인합니다."),
    ("coupon", "쿠폰 중복", "한 상품에는 쿠폰 한 장만 사용할 수 있습니다. 적립금과 쿠폰의 동시 사용은 가능합니다."),
    ("points", "적립금 소멸", "적립금 유효 기간은 지급일로부터 365일입니다. 만료된 적립금은 복원되지 않습니다."),
    ("membership", "멤버십 등급", "멤버십 등급은 최근 6개월의 구매 확정 금액으로 산정합니다. 매월 첫날 갱신합니다."),
    ("password", "비밀번호 재설정", "로그인 화면의 비밀번호 찾기에서 가입 이메일로 재설정 링크를 요청합니다. 링크는 30분 동안 유효합니다."),
    ("address", "배송지 변경", "배송지 변경은 결제 완료 상태에서만 가능합니다. 출고 준비가 시작되면 배송지 변경이 제한됩니다."),
    ("gift", "선물 주문", "선물 주문은 받는 사람이 3일 이내 배송지를 입력해야 합니다. 기한 내 입력이 없으면 주문이 자동 취소됩니다."),
    ("receipt", "현금 영수증", "현금 결제 주문의 현금 영수증은 구매 확정 이후 주문 상세에서 발급 신청합니다."),
    ("damage", "불량 상품 증빙", "상품 불량을 접수할 때 주문 번호, 불량 부위 사진, 상품 전체 사진을 첨부합니다. 사진만으로 판별이 어려우면 회수 검수를 진행합니다."),
    ("privacy", "개인정보 문의", "계정 삭제는 설정의 회원 탈퇴에서 신청합니다. 법정 보관 대상 거래 정보는 즉시 삭제되지 않을 수 있습니다."),
    ("support", "고객센터 운영", "고객센터 상담은 평일 10시부터 17시까지 운영합니다. 주말과 공휴일은 상담을 운영하지 않습니다."),
]
GROUPS = [
    ("dev", "return", "single", ["D01"], "수령 후 7일 이내, 미착용·택 유지", ["반품 접수는 수령 후 언제까지 가능한가요?", "옷 받은 지 5일 됐고 택 있어요. 반품 되나요?"]),
    ("test", "return_cost", "single", ["D02"], "단순 변심 3000원, 불량·오배송 판매자 부담", ["단순 변심 반품 배송비는 얼마인가요?", "색상이 맘에 안 들어 돌려보내면 택배비 얼마죠?"]),
    ("test", "exchange", "multi", ["D03", "D04"], "7일 이내, 재고 필요, 단순 변심 왕복 6000원", ["사이즈 교환 가능 기간과 왕복 배송비를 알려주세요.", "작아서 큰 걸로 바꾸고 싶어요. 언제까지고 비용은요?"]),
    ("dev", "refund", "single", ["D05"], "검수 후 영업일 3일 이내 요청, 카드사 반영 별도", ["반품 검수 후 환불 요청까지 얼마나 걸리나요?", "검수 끝났는데 돈 언제 들어와요? 카드요."]),
    ("test", "cancel", "single", ["D06"], "출고 준비 이후 취소 제한, 배송 후 반품", ["출고 준비 중인 주문 취소가 가능한가요?", "이미 포장 중이라는데 안 받고 취소할 수 있나요?"]),
    ("dev", "delivery", "single", ["D07"], "출고 후 영업일 2~4일, 예약 상품 별도", ["일반 배송은 출고 후 며칠 걸리나요?", "보냈다는데 이번 주 받을 수 있을까요?"]),
    ("test", "island", "single", ["D08"], "제주 추가 3000원, 도서 산간 결제 화면 확인", ["제주 지역 추가 배송비는 얼마인가요?", "제주도로 보내면 돈 더 내야 해요?"]),
    ("dev", "coupon", "single", ["D09"], "상품당 쿠폰 한 장, 적립금 병용 가능", ["쿠폰 두 장을 한 상품에 중복 적용할 수 있나요?", "쿠폰이랑 포인트 같이 써도 되나요?"]),
    ("test", "points", "single", ["D10"], "365일, 만료 후 복원 불가", ["적립금 유효 기간과 만료 후 복원 가능 여부는?", "포인트 기한 지나서 사라졌는데 살릴 수 있나요?"]),
    ("dev", "membership", "single", ["D11"], "최근 6개월 구매 확정 금액, 매월 첫날", ["멤버십 등급 산정 기간은 얼마나 되나요?", "회원 등급은 언제 바뀌고 뭐 보고 정하나요?"]),
    ("test", "password", "single", ["D12"], "가입 이메일 링크, 30분 유효", ["비밀번호 재설정 링크는 얼마 동안 유효한가요?", "비번 찾기 메일을 한 시간 뒤에 눌러도 되나요?"]),
    ("dev", "address", "single", ["D13"], "결제 완료 상태만 가능", ["배송지 변경은 어떤 주문 상태에서 가능한가요?", "주소를 잘못 적었는데 포장 시작했대요. 수정 되나요?"]),
    ("test", "gift", "single", ["D14"], "3일 이내 입력, 미입력 자동 취소", ["선물 받는 사람의 배송지 입력 기한은?", "선물 받은 친구가 주소 안 쓰면 어떻게 돼요?"]),
    ("dev", "receipt", "single", ["D15"], "구매 확정 후 주문 상세에서 신청", ["현금 영수증은 어디에서 언제 신청하나요?", "계좌로 결제했어요. 영수증 발급 받고 싶어요."]),
    ("dev", "damage", "multi", ["D02", "D16"], "주문 번호와 사진, 반품 비용은 판매자 부담", ["불량 상품 반품의 증빙과 배송비 부담은?", "옷이 찢어져 왔어요. 사진 뭘 보내고 반품비 누가 내죠?"]),
    ("test", "support", "single", ["D18"], "평일 10~17시, 주말·공휴일 미운영", ["고객센터 평일 상담 시간과 주말 운영 여부는?", "토요일 저녁에 상담원 연결 가능한가요?"]),
    ("dev", "international", "unanswerable", [], "해외 배송 정책 정보 없음", ["해외 배송이 가능한 국가를 알려주세요.", "캐나다로 보내는 운임은 얼마죠?"]),
    ("test", "resale", "unanswerable", [], "중고 매입 정책 정보 없음", ["중고 상품 매입 가격은 어떻게 정하나요?", "입던 옷 팔면 얼마 주나요?"]),
    ("dev", "repair", "unanswerable", [], "수선 정책 정보 없음", ["바지 기장 수선 비용을 알려주세요.", "소매 줄이는 서비스도 무료인가요?"]),
    ("test", "authentic", "unanswerable", [], "정품 감정 정책 정보 없음", ["정품 감정서 발급 비용은 얼마인가요?", "진품인지 감별해주는 서비스 있나요?"]),
    ("dev", "price", "unanswerable", [], "가격 보상 정책 정보 없음", ["구매 다음 날 가격이 내리면 차액 보상이 되나요?", "어제 샀는데 할인하네요. 차액 돌려주세요."]),
    ("test", "tax", "unanswerable", [], "해외 관세 정보 없음", ["해외 주문 관세는 누가 부담하나요?", "미국으로 주문하면 세금 얼마나 붙어요?"]),
    ("dev", "delivery_time", "unanswerable", [], "개별 택배 실시간 위치 없음", ["내 주문이 오늘 몇 시에 도착하나요?", "지금 택배 기사님 위치 좀 알려주세요."]),
    ("test", "stock", "unanswerable", [], "개별 상품 실시간 재고 없음", ["검정 운동화 270 사이즈 현재 재고는?", "그 신발 내일 재입고 몇 시죠?"]),
]

def main():
    docs = [dict(id=f"D{i:02}", topic=topic, title=title, text=text,
                 status="current", version="2026-11-01", source="authored-fiction")
            for i, (topic, title, text) in enumerate(POLICIES, 1)]
    for i, (title, text) in enumerate([
        ("반품 접수 이전 정책", "반품 접수는 수령 후 14일 이내 가능합니다. 2025년 폐기된 규정입니다."),
        ("반품 배송비 이전 정책", "단순 변심 반품 배송비는 무료입니다. 2025년 폐기된 규정입니다."),
        ("적립금 이전 정책", "적립금 유효 기간은 90일이며 만료 후 복원이 가능합니다. 폐기된 규정입니다."),
        ("상담 시간 이전 정책", "고객센터는 주말 포함 매일 24시간 상담합니다. 폐기된 규정입니다."),
    ], 19):
        docs.append(dict(id=f"D{i:02}", topic="archive", title=title, text=text,
                         status="archived", version="2025-01-01", source="authored-fiction"))
    questions = []
    for n, (split, group, kind, gold, answer, texts) in enumerate(GROUPS, 1):
        for j, query in enumerate(texts):
            questions.append(dict(id=f"Q{n:02}{chr(97+j)}", group=group, split=split,
                slice=kind, style="direct" if j == 0 else "conversational", query=query,
                gold_ids=gold, answerable=bool(gold), reference=answer,
                provenance="author-written synthetic teaching case", review="teaching-reference-v1"))
    OUT.mkdir(parents=True, exist_ok=True)
    for name, values in [("documents", docs), ("questions", questions)]:
        (OUT / f"{name}.json").write_text(json.dumps(values, ensure_ascii=False, indent=2)+"\n")
    print(f"{len(docs)} fictional documents; {len(questions)} questions; {len(GROUPS)} groups")

if __name__ == "__main__":
    main()
