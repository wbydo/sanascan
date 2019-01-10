import { Dispatch } from "redux";

import * as types from "./types";
import * as actions from "./actions";

import { RootState } from "../..";
import { actions as cursolActions } from "../../state/cursol";
import { actions as timerActions } from "../../state/timer";

import { setTimeoutPromise } from "../../util";

import { Action as _Action } from "../../util";

type Action = _Action<typeof actions>;

interface Store {
  getState: () => RootState;
  dispatch: Dispatch;
}

type Middleware = (store: Store) => (next: Dispatch) => (action: Action) => void;

export const middleware: Middleware
    = (store: Store) => (next: Dispatch) => (action: Action) => {

  const state = store.getState();
  switch (action.type) {
    case types.START:
      next(action);
      if (!state.timer.isActive) {
        const id = Date.now();
        next(timerActions.setActive(true));
        next(timerActions.setId(id));
        setTimeoutPromise(state.timer.scanSpeed).then(() => {
          store.dispatch(actions.finish(id));
        });
      }
      break;

    case types.FINISH:
      next(action);
      if (state.timer.isActive === false) {
        break;
      }

      next(timerActions.setActive(false));
      if (action.payload.id === state.timer.id) {
        next(cursolActions.increment());
        store.dispatch(actions.start());
      }

      break;

    default:
      next(action);
  }
};
