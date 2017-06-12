from fin360 import Fin360Client

fin360 = Fin360Client(access_token='7eseqecied5rbsdn95uovrc7j4hgtsg0')
statement = {
    "bank": "AXIS",
    "emailAddress": "madhu@loanzen.in",
    "accountType": "SAVING",
    "bankStmt": "2015_2016_statement.pdf"
}
fin360.upload_statement(statement)
# print fin360.get_transactions("e8p0dn04isohncqeciot7aurvi")
# print fin360.authenticate("madhu@loanzen.in", "Loanzen21")
# print fin360.upload_statement("ICICI", "SAVINGS")

# print fin360.get_transactions_with_details("jfkgl825s6nn4seau82r8rc3o4")