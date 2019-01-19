import { Dispatch } from "redux";

import * as types from "./types";
import * as actions from "./actions";

import { Store } from "../util";

import { Action as _Action } from "../../util";
type Action = _Action<typeof actions>;
import { actions as developerModeActions } from "../../state/developerMode";

const toggleEstimator = (store: Store) => {
  const { developerMode: { estimator }} = store.getState();
  store.dispatch(developerModeActions.setEstimatorActivity(!estimator));
};

const middleware
    = (store: Store) => (next: Dispatch) => (action: Action) => {

  switch (action.type) {
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
