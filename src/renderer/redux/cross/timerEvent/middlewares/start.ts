import { Dispatch } from "redux";

import { Store } from ".";

import * as types from "../types";
import * as actions from "../actions";

import { actions as timerActions } from "../../../state/timer";
import { setTimeoutPromise } from "../../../util";

export const middleware
    = (store: Store) => (next: Dispatch) => (action: ReturnType<typeof actions.start>) => {

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

    default:
      next(action);
  }
};
