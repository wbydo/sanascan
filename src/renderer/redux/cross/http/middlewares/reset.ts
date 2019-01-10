import { Dispatch } from "redux";

import { Store } from ".";

import * as actions from "../actions";
import * as types from "../types";

import { actions as timerEventActions } from "../../timerEvent";

import { RootState } from "../../..";
import { actions as estimatorActions } from "../../../state/estimator";

import { url as baseUrl } from "../../../../constant";
import SanascanError from "../../../../error";

type Action = ReturnType<typeof actions.reset>;

const reset = async (next: Dispatch, action: Action, state: RootState, storeDispatch: Dispatch) => {
  next(action);
  storeDispatch(timerEventActions.kill());

  const id = state.estimator.id;
  if (id === null) {
    throw new SanascanError();
  }

  const url = new URL(id!.toString(), baseUrl);
  await fetch(url.toString(), {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    method: "DELETE",
  });
  storeDispatch(estimatorActions.setResult(""));
  storeDispatch(timerEventActions.start());
};

export const middleware
    = (store: Store) => (next: Dispatch) => (action: Action) => {

  switch (action.type) {
    case types.RESET:
      reset(next, action, store.getState(), store.dispatch);
      break;

    default:
      next(action);
  }
};
