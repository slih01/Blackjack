import math
import random

try:
    import tkinter
except ImportError:  # python 2
    import Tkinter as tkinter


def load_images(card_images):
    suits = ["heart", "spade", "club", "diamond"]
    face_cards = ["jack", "queen", "king"]

    if tkinter.TkVersion >= 8.6:
        extension = "png"
    else:
        extension = "ppm"
    for suit in suits:
        for card in range(1, 11):
            name = "cards\\{}_{}.{}".format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((card, image))
        for face_card in face_cards:
            name = "cards\\{}_{}.{}".format(str(face_card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((10, image))


def deal_card(frame):
    # pop the next card of the top of deck
    top_card = deck.pop(0)
    deck.append(top_card)
    tkinter.Label(frame, image=top_card[1], relief="raised").pack(side="left")
    # return the cards face value:
    return top_card


def score_hand(hand):
    score = 0
    ace = False
    for card in hand:
        card_value = card[0]
        if card_value == 1 and not ace:
            ace = True
            card_value = 11
        score += card_value
        if score > 21 and ace:
            ace = False
            score -= 10
    return score


def deal_dealer():
    dealer_score = score_hand(dealer_hand)
    while 0 < dealer_score < 17:
        dealer_hand.append(deal_card(dealer_card_frame))
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


def deal_player():
    player_hand.append(deal_card(player_card_frame))
    player_score = score_hand(player_hand)
    player_score_label.set(player_score)
    if player_score > 21:
        result_text.set("You've bust!")

    # global player_score
    # global player_ace
    # card_value = deal_card(player_card_frame)[0]
    # if card_value == 1 and not player_ace:
    #     player_ace = True
    #     card_value = 11
    # if player_score > 21 and player_ace:
    #     player_score -= 10
    #     player_ace = False
    # player_score += card_value
    # player_score_label.set(player_score)
    # if player_score > 21:
    #     result_text.set("Dealer Wins")


def reset_cards():
    global dealer_card_frame
    global player_card_frame
    global dealer_hand
    global player_hand
    dealer_card_frame.destroy()
    dealer_card_frame = tkinter.Frame(card_frame, background="green")
    dealer_card_frame.grid(row=0, column=1, sticky="ew", rowspan=2)
    player_card_frame.destroy()
    player_card_frame = tkinter.Frame(card_frame, background="green")
    player_card_frame.grid(row=2, column=1, sticky="ew", rowspan=2)
    result_text.set("")
    dealer_hand = []
    player_hand = []

    deal_player()
    dealer_hand.append(deal_card(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand))
    deal_player()


mainWindow = tkinter.Tk()

mainWindow.title("Black Jack")
mainWindow.geometry("640x480")
mainWindow.config(background="green")

result_text = tkinter.StringVar()
result = tkinter.Label(mainWindow, textvariable=result_text)
result.grid(row=0, column=0, columnspan=3)

card_frame = tkinter.Frame(mainWindow, relief="sunken", borderwidth=1, background="green")
card_frame.grid(row=1, column=0, sticky="ew", columnspan=3, rowspan=2)

dealer_score_label = tkinter.IntVar()
tkinter.Label(card_frame, text="Dealer", fg="white", background="green").grid(row=0, column=0)
tkinter.Label(card_frame, textvariable=dealer_score_label, fg="white", background="green").grid(row=1, column=0)
# embedded frame to hold the card images
dealer_card_frame = tkinter.Frame(card_frame, background="green")
dealer_card_frame.grid(row=0, column=1, sticky="ew", rowspan=2)

player_score_label = tkinter.IntVar()
tkinter.Label(card_frame, text="Player", fg="white", background="green").grid(row=2, column=0)
tkinter.Label(card_frame, textvariable=player_score_label, fg="white", background="green").grid(row=3, column=0)
player_card_frame = tkinter.Frame(card_frame, background="green")
player_card_frame.grid(row=2, column=1, sticky="ew", rowspan=2)

button_frame = tkinter.Frame(mainWindow)
button_frame.grid(row=3, column=0, columnspan=3, sticky="w")
dealer_button = tkinter.Button(button_frame, text="Dealer", relief="raised", borderwidth=1, command=deal_dealer)
dealer_button.grid(row=0, column=0, sticky="ew")
player_button = tkinter.Button(button_frame, text="Player", relief="raised", borderwidth=1, command=deal_player)
player_button.grid(row=0, column=1, sticky="ew")

reset_button = tkinter.Button(mainWindow, text="New Game", command=reset_cards)
reset_button.grid(row=4, column=0)

# load cards
cards = []
load_images(cards)

# create a new deck and shuffle
# could say deck = cards but then cards would be removed from cards. By creating a new list cards remains untouched
deck = list(cards)*3
random.shuffle(deck)

dealer_hand = []
player_hand = []

deal_player()
dealer_hand.append(deal_card(dealer_card_frame))
dealer_score_label.set(score_hand(dealer_hand))
deal_player()

mainWindow.mainloop()
