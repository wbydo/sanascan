export const chars: string[][] = [
  ["あ", "か", "さ", "た", "な", "は", "ま", "や", "ら", "わ"],
  ["い", "き", "し", "ち", "に", "ひ", "み", "",   "り", ""],
  ["う", "く", "す", "つ", "ぬ", "ふ", "む", "ゆ", "る", "を"],
  ["え", "け", "せ", "て", "ね", "へ", "め", "",   "れ", ""],
  ["お", "こ", "そ", "と", "の", "ほ", "も", "よ", "ろ", "ん"],
];

export const MAX_COLUMN_INDEX = chars[0].length - 1;
export const MAX_ROW_INDEX = chars.length - 1;

export const url = "http://localhost:8000";
