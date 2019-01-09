import { Dispatch } from "redux";

import { RootState } from "..";

import { cursolActions } from "../cursol/index";

import { start, finish, setActive, setId } from "./actions";
import { Action } from "./reducers";
import * as types from "./types";

import { setTimeoutPromise } from "../util";

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
      next(action);
      if (!state.timer.isActive) {
        const id = Date.now();
        next(setActive(true));
        next(setId(id));
        setTimeoutPromise(state.timer.scanSpeed).then(() => {
          store.dispatch(finish(id));
        });
      }
      break;

    case types.FINISH:
      next(action);
      if (state.timer.isActive === false) {
        break;
      }

      next(setActive(false));
      if (action.payload.id === state.timer.id) {
        next(cursolActions.increment());
        store.dispatch(start());
      }

      break;

    default:
      next(action);
  }
};

export default middleware;
