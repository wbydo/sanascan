import { Dispatch } from "redux";

import { Store } from ".";

import * as actions from "../actions";
import * as types from "../types";

import { actions as timerActions } from "../../../state/timer";
import { actions as cursolActions } from "../../../state/cursol";

export const middleware
    = (store: Store) => (next: Dispatch) => (action: ReturnType<typeof actions.finish>) => {

  const state = store.getState();
  switch (action.type) {
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
