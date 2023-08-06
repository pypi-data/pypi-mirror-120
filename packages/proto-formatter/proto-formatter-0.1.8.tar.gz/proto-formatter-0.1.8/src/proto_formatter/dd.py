from src.proto_formatter import format_str

proto_str = """
    /*
    Person balabala
*/
    message Person {
    // comment of name a
    // https:github.skyscannertools.net/fbi-partners/ndc-as-config/blob/master/engine/farelogix/templates/SeatAvailabilityRQ.xml#L18
required string name = 1; // comment of name b
/* 
comment of id a
// comment of id b
         */
        required int32 id = 2;// comment of id c
       optional string email = 3;// comment of email
}
"""
formatted_proto_str = format_str(proto_str, align_by_equal_sign=True, comment_max_length=120)
print(formatted_proto_str)