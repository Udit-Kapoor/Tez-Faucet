import smartpy as sp 

class Faucet(sp.Contract):
        def __init__(self , _admin):
            self.init(
            #Storage
            admin = _admin,
            amount = sp.mutez(0) , #for every claim
            balance = sp.mutez(0),    #to maintain balance

            ledger = sp.big_map(
                tkey = sp.TAddress,
                tvalue = sp.TNat),
            )

        @sp.entry_point
        def claim(self):
            sp.verify(~self.data.ledger.contains(sp.source) , "USER_ALREADY_CLAIMED" )  #condition , message)
            sp.send(sp.source , self.data.amount)
            self.data.balance -= self.data.amount

            self.data.ledger[sp.source] = 1;

        @sp.entry_point
        def addBalance(self , amount , balance):
            sp.verify(sp.sender == self.data.admin , "NOT_ADMIN")
            sp.verify(sp.amount == balance , "AMOUNT_MISMATCH")

            self.data.balance += balance
            self.data.amount = amount

        @sp.entry_point
        def withdraw(self):
            sp.verify(sp.sender == self.data.admin , "NOT_ADMIN")
            sp.send(self.data.admin , self.data.balance)
            self.data.balance = sp.mutez(0)

        @sp.entry_point
        def updateAdmin(self , newAdmin):
            sp.verify(sp.sender == self.data.admin , "NOT_ADMIN")
            self.data.admin = newAdmin

if "templates" not in __name__:
    @sp.add_test(name = "Faucet")
    def test():
        scenario = sp.test_scenario()
        alice = sp.test_account("alice")
        bob = sp.test_account("bob")
        admin = sp.test_account("admin")


        c = Faucet(_admin = admin.address)

        scenario+= c

        c.addBalance(amount = sp.mutez(1000000) , balance = sp.mutez(1000000000)).run(sender = admin , amount = sp.tez(1000))

        c.claim().run(sender = alice)
        c.claim().run(sender = bob)

        

