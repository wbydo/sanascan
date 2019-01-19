import { Dispatch } from "redux";

import * as types from "./types";
import * as actions from "./actions";

import { Store } from "../util";
import { actions as timerActions } from "../timer";

import { Action as _Action } from "../../util";
type Action = _Action<typeof actions>;
import { actions as developerModeActions } from "../../state/developerMode";

const toggleTimer = (store: Store) => {
  const { developerMode: { timer }} = store.getState();
  store.dispatch(developerModeActions.setTimerActivity(!timer));

  if (timer) {
    store.dispatch(timerActions.kill());
  } else {
    store.dispatch(timerActions.start());
  }
};

const toggleEstimator = (store: Store) => {
  const { developerMode: { estimator }} = store.getState();
  store.dispatch(developerModeActions.setEstimatorActivity(!estimator));
};

const middleware
    = (store: Store) => (next: Dispatch) => (action: Action) => {

  switch (action.type) {
    case types.TOGGLE_TIMER:
      next(action);
      toggleTimer(store);
      break;

    case types.TOGGLE_ESTIMATOR:
      next(action);
      toggleEstimator(store);
      break;

    default:
      next(action);
      break;
  }
};

export const middlewares = [
  middleware,
];
