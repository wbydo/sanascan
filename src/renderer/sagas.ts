import { delay } from "redux-saga";
import { put, all } from "redux-saga/effects";

import { increment } from "./actions";

// export function* incrementAsync(): IterableIterator<any> {
//   while(true){
//     yield delay(1000);
//     yield put(increment());
//   }
// }
//
// export default function* rootSaga(): Iterable<any> {
//   while(true){
//     yield incrementAsync();
//   }
// }
