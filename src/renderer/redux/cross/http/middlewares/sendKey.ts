import { Dispatch } from "redux";
import { stringify } from "querystring";

import { Store } from ".";

import * as actions from "../actions";
import * as types from "../types";

import { RootState } from "../../..";
import { actions as estimatorActions } from "../../../state/estimator";

import SanascanError from "../../../../error";
import { url as baseUrl } from "../../../../constant";

const sendKey = (next: Dispatch, action: ReturnType<typeof actions.sendKey>, state: RootState) => {
  next(action);

  const id = state.estimator.id;
  if (id === null) {
    throw new SanascanError();
  }

  const url = new URL(id.toString(), baseUrl);
  const query = stringify({key: action.payload.key.toString()});
  fetch(url.toString(), {
    body: query.toString(),
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    method: "POST",
  }).then((resp) => {
    return Promise.resolve(resp.json());
  }).then((json) => {
    if (json.result === undefined) {
      throw new SanascanError();
    }
    next(estimatorActions.setResult(json.result));
  });
};

export const middleware
    = (store: Store) => (next: Dispatch) => (action: ReturnType<typeof actions.sendKey>) => {

  switch (action.type) {
    case types.SEND_KEY:
      sendKey(next, action, store.getState());
      break;

    default:
      next(action);
  }
};
