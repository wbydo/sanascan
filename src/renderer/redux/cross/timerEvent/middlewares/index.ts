import { Dispatch } from "redux";

import * as types from "../types";
import * as actions from "../actions";

import { actions as timerActions } from "../../../state/timer";
import { actions as cursolActions } from "../../../state/cursol";

import { Action as _Action } from "../../../util";
import { setTimeoutPromise } from "../../../util";

import { RootState } from "../../..";

type Action = _Action<typeof actions>;

export interface Store {
  getState: () => RootState;
  dispatch: Dispatch;
}

const middleware
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

    case types.KILL:
      next(action);
      next(timerActions.setActive(false));
      break;

    default:
      next(action);
  }
};

export const middlewares = [
  middleware,
];
