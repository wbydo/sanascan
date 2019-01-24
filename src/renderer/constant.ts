export const chars: string[][] = [
  ["あ", "か", "さ", "た", "な", "は", "ま", "や", "ら", "わ", "ゃ"],
  ["い", "き", "し", "ち", "に", "ひ", "み", "ゆ", "り", "を", "ゅ"],
  ["う", "く", "す", "つ", "ぬ", "ふ", "む", "よ", "る", "ん", "ょ"],
  ["え", "け", "せ", "て", "ね", "へ", "め", "",   "れ", "",  "っ"],
  ["お", "こ", "そ", "と", "の", "ほ", "も", "",   "ろ", "",  "ー"],
];

export const MAX_COLUMN_INDEX = chars[0].length - 1;
export const MAX_ROW_INDEX = chars.length - 1;

export const url = "http://localhost:8000";
