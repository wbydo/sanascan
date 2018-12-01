import { Dispatch } from "redux";

import { RootState } from "../index";

import { cursolActions } from "../cursol/index";

import { Action, start, finish, runMiddleware, setActive } from "./actions";
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

  const state = store.getState();
  switch (action.type) {
    case types.START:
      next(runMiddleware());
      if (!state.window.timer.isActive) {
        next(setActive(true));
        setTimeoutPromise(state.window.timer.scanSpeed).then(() => {
          middleware(store)(next)(finish());
        });
      }
      break;

    case types.FINISH:
      next(runMiddleware());
      if (state.window.timer.isActive) {
        next(cursolActions.increment());
        next(setActive(false));
        middleware(store)(next)(start());
      }
      break;

    default:
      next(action);
  }
};

export default middleware;
