import { Dispatch } from "redux";

import { RootState } from "./reducers";
import { Action, increment } from "./actions";
import * as types from "./types";

interface Store {
  getState: () => RootState;
  dispatch: Dispatch;
}

type Middleware = (store: Store) => (next: Dispatch) => (action: Action) => void

const setTimeoutPromise = (delay: number) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve();
    },
    delay);
  });
};

export const middleware: Middleware
    = (store: Store) => (next: Dispatch) => (action: Action) => {

  if (action.type === types.START_INCREMENT) {
    setTimeoutPromise(1000).then(() => {
      next(increment());
    });
  }
};
