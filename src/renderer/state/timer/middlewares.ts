import { Dispatch } from "redux";

import { RootState } from "../reducers";

import { cursolActions } from "../cursol/index";

import { Action, start, finish, setActive } from "./actions";
import * as types from "./types";

import { setTimeoutPromise } from "../../myutil";

interface Store {
  getState: () => RootState;
  dispatch: Dispatch;
}

type Middleware = (store: Store) => (next: Dispatch) => (action: Action) => void;

const middleware: Middleware
    = (store: Store) => (next: Dispatch) => (action: Action) => {

  const state = store.getState();
  switch (action.type) {
    case types.START:
      if (!state.timer.isActive) {
        next(setActive(true));
        setTimeoutPromise(state.timer.scanSpeed).then(() => {
          store.dispatch(finish());
        });
      }
      break;

    case types.FINISH:
      if (state.timer.isActive) {
        next(cursolActions.increment());
        next(setActive(false));
        store.dispatch(start());
      }
      break;

    default:
      next(action);
  }
};

export default middleware;
