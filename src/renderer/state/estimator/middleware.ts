import { Dispatch } from "redux";

import { RootState } from "../reducers";

import * as types from "./types";
import * as actions from "./actions";

import { url } from "../../constant";

import SanascanError from "../../error";

import { setTimeoutPromise } from "../../myutil";

interface Store {
  getState: () => RootState;
  dispatch: Dispatch;
}

type Middleware = (store: Store) => (next: Dispatch) => (action: actions.Action) => void;

const TRY_NUMBER = 10;
const TIMEOUT = 5000;

const tryFethIdOnce = async (next: Dispatch) => {
  const response = await fetch(url, {method: "POST"});
  const result = await response.json();

  if (result.eid !== undefined && (typeof result.eid === "number")) {
    next(actions.fetchId("done"));
    next(actions.setId(result.eid as number));
    return;
  } else {
    throw new SanascanError();
  }
};

const fetchIdStart = async (next: Dispatch) => {
  let isSuccess = false;
  for (const _ of Array(TRY_NUMBER).keys()) {
    if (isSuccess) {
      break;
    }
    try {
      await tryFethIdOnce(next).then(() => { isSuccess = true; });
    } catch (err) {
      await setTimeoutPromise(TIMEOUT);
    }
  }

  if (!isSuccess) {
    next(actions.fetchId("error"));
  }
};

const processFetchIdAction = (next: Dispatch, action: actions.Action) => {
  switch (action.payload.status) {
    case "start":
      next(action);
      fetchIdStart(next);
      break;
  }
};

const middleware: Middleware
    = (store: Store) => (next: Dispatch) => (action: actions.Action) => {

  switch (action.type) {
    case types.FETCH_ID:
      if (action.payload.status === undefined) {
        throw new SanascanError();
      }
      processFetchIdAction(next, action);
      break;

    default:
      next(action);
  }
};

export default middleware;
