import { delay, SagaIterator } from "redux-saga";
import { put, takeEvery, call, all } from "redux-saga/effects";

import { ASYNC_INCREMENT } from "./types";

import { increment } from "./actions";

export function* incrementAsync() {
  yield delay(1000);
  yield put(increment());
}

function* watchAsyncIncrement() {
  yield takeEvery(ASYNC_INCREMENT, incrementAsync);
}

export default function* rootSaga() {
  yield all([
    call(watchAsyncIncrement),
  ]);
}
