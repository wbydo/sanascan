import { Dispatch } from "redux";

import { RootState } from "../reducers";
import { increment } from "../actions";

import { Action, start, finish } from "./actions";
import * as types from "./types";

interface Store {
  getState: () => RootState;
  dispatch: Dispatch;
}

type Middleware = (store: Store) => (next: Dispatch) => (action: Action) => void;

const setTimeoutPromise = (delay: number) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve();
    },
    delay);
  });
};

const middleware: Middleware
    = (store: Store) => (next: Dispatch) => (action: Action) => {

  switch (action.type) {
    case types.START:
      next(start());
      setTimeoutPromise(1000).then(() => {
        next(finish());
      });
      break;

    case types.FINISH:
      break;

    default:
      next(action);
  }
};

export default middleware;
