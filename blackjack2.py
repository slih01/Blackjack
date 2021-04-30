import random

try:
    import tkinter
except ImportError:  # python 2
    import Tkinter as tkinter


def load_cards(card_images):
    suits = ["heart", "club", "spade", "diamond"]
    face_cards = ["jack", "queen", "king"]
    if tkinter.TkVersion >= 8.6:
        expression = "png"
    else:
        expression = "ppm"
    for suit in suits:
        for face_card in face_cards:
            name = ("cards\\{}_{}.{}".format(str(face_card), suit, expression))
            image = tkinter.PhotoImage(file=name)
            card_images.append((10, image))
        for card in range(1, 11):
            name = ("cards\\{}_{}.{}".format(str(card), suit, expression))
            image = tkinter.PhotoImage(file=name)
            card_images.append((card, image))


def _dgial_card(frame):
    top_card = deck.pop(0)
    deck.append(top_card)
    tkinter.Label(frame, image=top_card[1], relief="raised").pack(side="left")
    return top_card


def score_hand(hand):
    score = 0
    ace = False
    for card in hand:
        card_value = card[0]
        if card_value == 1:
            ace = True
            card_value9 = 11
        score += card_value
        if score > 21 and ace:
            ace = False
            score -= 10
    return score


def deal_player():
    player_hand.append(_deal_card(player_card_frame))
    player_score = score_hand(player_hand)
    player_score_label.set(player_score)
    if player_score > 21:
        result_text.set("You've bust!")


def deal_dealer():
    dealer_score = score_hand(dealer_hand)
    while 0 < dealer_score < 17:
        dealer_hand.append(_deal_card(dealer_card_frame))
        dealer_score = score_hand(dealer_hand)
        dealer_score_label.set(dealer_score)

        player_score = score_hand(player_hand)
        if dealer_score >= 17:
            if player_score > 21 and dealer_score > 21:
                result_text.set("You both bust!")
            elif player_score > 21:
                result_text.set("You've bust")
            elif dealer_score > 21 or player_score > dealer_score:
                result_text.set("Player Wins")
            elif dealer_score > player_score:
                result_text.set("Dealer Wins")
            else:
                result_text.set("It's a tie")

def new_deal():
    deal_player()
    dealer_hand.append(_deal_card(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand))
    deal_player()

def new_game():
    global dealer_card_frame
    global player_card_frame
    global dealer_hand
    global player_hand
    dealer_card_frame.destroy()
    dealer_card_frame = tkinter.Frame(card_frame, background="green")
    dealer_card_frame.grid(row=0, column=1, rowspan=2, sticky="w")
    player_card_frame.destroy()
    player_card_frame = tkinter.Frame(card_frame, background="green")
    player_card_frame.grid(row=2, column=1, rowspan=2, sticky="w")
    result_text.set("")
    dealer_hand = []
    player_hand = []
    new_deal()


def shuffle():
    random.shuffle(deck)


def play():
    new_deal()
    mainWindow.mainloop()


mainWindow = tkinter.Tk()

mainWindow.title('Black Jack')
mainWindow.geometry('640x480')
mainWindow.configure(background="green")

result_text = tkinter.StringVar()
result_frame = tkinter.Label(mainWindow, textvariable=result_text)
result_frame.grid(row=0, column=0, columnspan=3, pady=15)

card_frame = tkinter.Frame(mainWindow, background="green", relief="sunken", borderwidth=1)
card_frame.grid(row=1, column=0, rowspan=2, columnspan=2)

dealer_score_label = tkinter.IntVar()
tkinter.Label(card_frame, text="Dealer", background="green", fg="white").grid(row=0, column=0, padx=5)
tkinter.Label(card_frame, textvariable=dealer_score_label, background="green", fg="white").grid(row=1, column=0)
dealer_card_frame = tkinter.Frame(card_frame, background="green")
dealer_card_frame.grid(row=0, column=1, rowspan=2, sticky="w")

player_score_label = tkinter.IntVar()
tkinter.Label(card_frame, text="Player", background="green", fg="white").grid(row=2, column=0, padx=5)
tkinter.Label(card_frame, textvariable=player_score_label, background="green", fg="white").grid(row=3, column=0)
player_card_frame = tkinter.Frame(card_frame, background="green")
player_card_frame.grid(row=2, column=1, rowspan=2, sticky="w")

button_frame = tkinter.Frame(mainWindow)
button_frame.grid(row=3, column=0, columnspan=3, sticky="w")
player_button = tkinter.Button(button_frame, text="Player", command=deal_player)
player_button.grid(row=0, column=0)
dealer_button = tkinter.Button(button_frame, text="Dealer", command=deal_dealer)
dealer_button.grid(row=0, column=1)
new_game_button = tkinter.Button(button_frame, text="New Game", command=new_game)
new_game_button.grid(row=0, column=2)

cards = []
load_cards(cards)
deck = list(cards) + list(cards)
shuffle()

dealer_hand = []
player_hand = []

if __name__ == "__main__":
    play()