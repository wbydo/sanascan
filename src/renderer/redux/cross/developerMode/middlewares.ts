import { Dispatch } from "redux";

import * as types from "./types";
import * as actions from "./actions";

import { Store } from "../util";
import { actions as timerActions } from "../timer";

import { Action as _Action } from "../../util";
type Action = _Action<typeof actions>;
import { actions as developerModeActions } from "../../state/developerMode";
import { actions as httpActions } from "../../cross/http";

const toggle = (store: Store) => {
  const { developerMode: { isActive }} = store.getState();
  store.dispatch(developerModeActions.setActive(!isActive));

  if (isActive) {
    store.dispatch(httpActions.fetchId("start"));
  } else {
    store.dispatch(timerActions.kill());
  }
};

const toggleTimer = (store: Store) => {
  const { developerMode: { timer }} = store.getState();
  store.dispatch(developerModeActions.setTimerActivity(!timer));

  if (timer) {
    store.dispatch(timerActions.kill());
  } else {
    store.dispatch(timerActions.start());
  }
};

const middleware
    = (store: Store) => (next: Dispatch) => (action: Action) => {

  switch (action.type) {
    case types.TOGGLE:
      next(action);
      toggle(store);
      break;

    case types.TOGGLE_TIMER:
      next(action);
      toggleTimer(store);
      break;

    default:
      next(action);
      break;
  }
};

export const middlewares = [
  middleware,
];
