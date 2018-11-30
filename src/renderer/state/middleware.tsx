import { Dispatch } from "redux";

import { RootState } from "./reducers";
import { Action, increment, startTimer, finishTimer } from "./actions";
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

export const middleware: Middleware
    = (store: Store) => (next: Dispatch) => (action: Action) => {

  switch (action.type) {
    case types.START_TIMER:
      setTimeoutPromise(1000).then(() => {
        next(finishTimer());
      });
      break;

    case types.FINISH_TIMER:
      break;
  }
};
