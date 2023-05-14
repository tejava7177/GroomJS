let deck = [];
let playerMoney = 100;
let betAmount = 0;


function createDeck() {
  const values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'];
  const suits = ["♠", "♥", "♦", "♣"];
  for (let valueIdx = 0; valueIdx < values.length; valueIdx++) {
    for (let suitIdx = 0; suitIdx < suits.length; suitIdx++) {
      let card = {
        value: values[valueIdx],
        suit: suits[suitIdx]
      };
      deck.push(card);
    }
  }
  shuffleDeck(deck);
  return deck;
}

function shuffleDeck(deck) {
  for (let i = 0; i < deck.length; i++) {
    let swapIdx = Math.floor(Math.random() * deck.length);
    let tmp = deck[swapIdx];
    deck[swapIdx] = deck[i];
    deck[i] = tmp;
  }
}

function getNextCard() {
  return deck.shift();
}

  function startGame() {
    // 게임 초기화
    deck = createDeck();
    playerHand = [];
    dealerHand = [];
    playerScore = 0;
    dealerScore = 0;
    gameStarted = true;
    gameOver = false;
    document.getElementById('player-cards').innerHTML = '';


    document.getElementById('start-btn').style.display = 'none';
    document.getElementById('dealer-score').textContent = 'Dealer : ???';
    document.getElementById('player-score').classList.remove('hidden');
    document.getElementById('player-cards').classList.remove('hidden');
    document.getElementById('bet').classList.remove('hidden');
    document.getElementById('hit-stand').classList.remove('hidden');
    document.getElementById('again-btn').style.display = 'none';
    
   
    // 베팅
    betAmount = parseInt(prompt("How much would you like to bet?"));
    while (isNaN(betAmount) || betAmount <= 0 || betAmount > playerMoney) {
    betAmount = parseInt(prompt("Invalid bet amount. Please enter a valid amount:"));
    }
    playerMoney -= betAmount;

    document.getElementById('player-money').textContent = 'Player Money: ' + playerMoney;
    document.getElementById('bet-Amount').textContent = 'Bet Amount: ' + betAmount;
    
    // 카드를 나눠줌
    playerHand.push(getNextCard());
    dealerHand.push(getNextCard());
    playerHand.push(getNextCard());
    dealerHand.push(getNextCard());
  
    

    // 화면 갱신
    updateScores();
    showStatus();
    

    //updatePlayerMoney();
  }


  
  function showStatus() {
    // 플레이어 카드 보여주기
    var playerCardString = '';
    for (var i = 0; i < playerHand.length; i++) {
      playerCardString += getCardString(playerHand[i]);
      document.getElementById('player-cards').innerHTML += '<div class="card">' + playerCardString + '</div>';
      playerCardString = '';
    }
  
    // 딜러 카드 보여주기
    var dealerCardString = '';
    for (var i = 0; i < dealerHand.length; i++) {
      dealerCardString += getCardString(dealerHand[i]) + '\n';
    }
  
    updateScores();
  
    // 화면에 보여주기
    
    //document.getElementById('dealer-cards').innerText = dealerCardString;
    // document.getElementById('player-score').innerText = 'Player: ' + playerScore;
    // document.getElementById('dealer-score').innerText = 'Dealer: ' + dealerScore;
    // document.getElementById('player-score').textContent = 'Player: ' + playerScore;
    // document.getElementById('dealer-score').textContent = 'Dealer: ' + dealerScore;

  
    // if (gameOver) {
    //   if (playerWon) {
    //     document.getElementById('status').innerText = "You won!";
    //   }
    //   else {
    //     document.getElementById('status').innerText = "Dealer won!";
    //   }
  
    //   document.getElementById('new-game').style.display = 'inline';
    //   document.getElementById('hit-button').style.display = 'none';
    //   document.getElementById('stay-button').style.display = 'none';
    // }

  }

  function getCardString(card) {
    return card.value + ' of ' + card.suit;
  }

  function updateScores() {
    dealerScore = getHandScore(dealerHand);
    playerScore = getHandScore(playerHand);
    //document.getElementById('dealer-score').textContent = 'Dealer: ' + dealerScore;
    document.getElementById('player-score').textContent = 'Player: ' + playerScore;
  }
  

  function getCardValue(card) {
    switch (card.value) {
      case 'A':
        return 1;
      case 'Two':
        return 2;
      case 'Three':
        return 3;
      case 'Four':
        return 4;
      case 'Five':
        return 5;
      case 'Six':
        return 6;
      case 'Seven':
        return 7;
      case 'Eight':
        return 8;
      case 'Nine':
        return 9;
      default:
        return 10;
    }
  }
  

function getHandScore(hand) {
    let score = 0;
    let aceCount = 0;
  
    for (let i = 0; i < hand.length; i++) {
        parseInt(hand[i].value);
        const card = hand[i].value;

      if (card === 'A') {
        aceCount++;
        score += 11;
      } else if (card === 'K' || card === 'Q' || card === 'J') {
        score += 10;
      } else {
        score += Number(card);
      }
    }
  
    while (score > 21 && aceCount > 0) {
      score -= 10;
      aceCount--;
    }
  
    return score;
  }
  
  //hit 함수
  function hit(hand) {
    hand.push(getNextCard());
    return hand[hand.length - 1];
  }
  

  function hitPlayer() {
    let card = hit(playerHand);
    let cardString = getCardString(card);
    let playerCards = document.getElementById('player-cards');
    playerCards.innerHTML += '<div class="card">' + cardString + '</div>';
    updateScores();

    if (playerScore > 21) {
        console.log('bust');
        alert("You bust!!");
        stand();
      }
  }
  


function stand() {
    // 딜러 카드 공개
    //revealDealerCards();
  
    // 딜러 카드 합계가 17 이하면 카드를 계속 뽑음
    while (dealerScore <= 17) {
      dealerHand.push(deck.shift());
      dealerScore = getHandScore(dealerHand);
      //renderDealerCards();
      document.getElementById('dealer-score').innerText = 'Dealer: ' + dealerScore;
    }
  
    document.getElementById('dealer-score').innerText = 'Dealer: ' + dealerScore;
    // 승자 판정
    console.log(playerMoney);
    console.log(betAmount);
    console.log(determineWinner());
    //alert(determineWinner() + "Win!!");

    document.getElementById('hit-stand').classList.add('hidden');
    //document.getElementById('again-btn').style.display = 'block'

    if(determineWinner()==="Player"){
        playerMoney = playerMoney + (betAmount * 2);
        alert(determineWinner() + "Win!!");
        console.log(playerMoney);
        document.getElementById('player-money').textContent = 'Player Money: ' + playerMoney;
        document.getElementById('bet-Amount').classList.add('hidden');
        document.getElementById('again-btn').style.display = 'block'
    }

    else if(determineWinner() === 'Dealer'){
        document.getElementById('again-btn').style.display = 'block'
        alert(determineWinner() + "Win!!");
        if(playerMoney == 0){
            console.log("Game Over");
            alert("Game Over");
            document.getElementById('again-btn').style.display = 'none'
            document.getElementById('reset-btn').style.display = 'block'
        }
      }
      
      else if(determineWinner() === 'Tie'){
        document.getElementById('again-btn').style.display = 'block'
        alert(determineWinner() + "!!");
        playerMoney = playerMoney + betAmount;
      }
    
  }


  function determineWinner() {
    if (playerScore > 21) {
      return 'Dealer';
    } else if (dealerScore > 21) {
      return 'Player';
    } else if (dealerScore > playerScore) {
      return 'Dealer';
    } else if (dealerScore < playerScore) {
      return 'Player';
    } else {
      return 'Tie';
    }
  }


//   function renderBetAndMoney() {
//     document.getElementById('player-money').innerText = 'Money: $' + playerMoney;
//     document.getElementById('bet-amount-display').innerText = 'Bet: $' + betAmount;
//   }
  


function resetGame() {
  // 게임 초기화
  deck = createDeck();
  playerHand = [];
  dealerHand = [];
  playerScore = 0;
  dealerScore = 0;
  gameStarted = false;
  gameOver = false;
  playerMoney = 100;
  betAmount = 0;

  // 화면 초기화
  document.getElementById('player-cards').innerHTML = '';
  document.getElementById('dealer-cards').innerHTML = '';
  document.getElementById('player-score').innerHTML = '';
  document.getElementById('dealer-score').innerHTML = '';
  document.getElementById('player-money').innerHTML = 'Your Money: ' + playerMoney;
  document.getElementById('bet-Amount').innerHTML = '';

  // 버튼 초기화
  document.getElementById('start-btn').style.display = 'block';
  document.getElementById('hit-btn').style.display = 'none';
  document.getElementById('stand-btn').style.display = 'none';
  document.getElementById('reset-btn').style.display = 'none';

}

