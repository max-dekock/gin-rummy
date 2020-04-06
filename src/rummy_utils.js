export const RANKS = ["A","2","3","4","5","6","7","8","9","T","J","Q","K"];
export const SUITS = ["s","h","d","c"];

let d = [];
for (let rank of RANKS) {
  for (let suit of SUITS) {
    d.push(rank + suit);
  }
}
export const DECK = d;

export function getRank(card) {
  return card.charAt(0);
}

export function getSuit(card) {
  return card.charAt(1);
}

export function isSet(cards) {
  if (cards.length < 3) {
    return false;
  }
  let r = new Set();
  for (let card of cards) {
    r.add(getRank(card));
  }
  return (r.size == 1);
}

export function isRun(cards) {
  if (cards.length < 3) {
    return false;
  }
  let s = new Set();
  let r = [];
  for (let card of cards) {
    s.add(getSuit(card));
    r.push(RANKS.indexOf(getRank(card)));
  }
  if (s.size > 1) {
    return false;
  }
  r.sort((a,b) => {return a-b;});
  let prev_i = -1;
  for (let i of r) {
    if (prev_i != -1 && i != prev_i + 1) {
      return false;
    } else {
      prev_i = i;
    }
  }
  return true;
}

export function isMeld(cards) {
  return (isSet(cards) || isRun(cards));
}

export function pointValue(card) {
  let rank = getRank(card);
  switch(rank) {
    case "A":
      return 1;
    case "T":
    case "J":
    case "Q":
    case "K":
      return 10;
    default:
      return parseInt(rank);
  }
}

export function deadwoodPoints(deadwood) {
  let v = 0;
  for (let card of deadwood) {
    v += pointValue(card);
  }
  return v;
}

export function shuffle(a) {
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    let t = a[i];
    a[i] = a[j];
    a[j] = t;
  }
}