import { delay, SagaIterator } from "redux-saga";
import { put, takeEvery, call, all } from "redux-saga/effects";

import { START_INCREMENT } from "./types";

import { increment } from "./actions";

export function* infinity_increment() {
  while (true) {
    yield delay(1000);
    yield put(increment());
  }
}

function* watchAsyncIncrement() {
  yield takeEvery(START_INCREMENT, infinity_increment);
}

export default function* rootSaga() {
  yield all([
    call(watchAsyncIncrement),
  ]);
}
