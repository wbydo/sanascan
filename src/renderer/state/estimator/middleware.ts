import { Dispatch } from "redux";

import { RootState } from "../reducers";

import * as types from "./types";
import * as actions from "./actions";

import { url } from "../../constant";

import SanascanError from "../../error";

import { setTimeoutPromise } from "../../myutil";

import { timerActions } from "../timer";

interface Store {
  getState: () => RootState;
  dispatch: Dispatch;
}

type Middleware = (store: Store) => (next: Dispatch) => (action: actions.Action) => void;

const TRY_NUMBER = 10;
const TIMEOUT = 5000;

const tryFethIdOnce = async (storeDispatch: Dispatch) => {
  const response = await fetch(url, {method: "POST"});
  const result = await response.json();

  if (result.eid !== undefined && (typeof result.eid === "number")) {
    storeDispatch(actions.fetchId("done"));
    storeDispatch(actions.setId(result.eid as number));
    return;
  } else {
    throw new SanascanError();
  }
};

const fetchIdStart = async (storeDispatch: Dispatch) => {
  let isSuccess = false;
  for (const _ of Array(TRY_NUMBER).keys()) {
    if (isSuccess) {
      break;
    }
    try {
      await tryFethIdOnce(storeDispatch).then(() => { isSuccess = true; });
    } catch (err) {
      await setTimeoutPromise(TIMEOUT);
    }
  }

  if (isSuccess) {
    storeDispatch(actions.fetchId("done"));
  } else {
    storeDispatch(actions.fetchId("error"));
  }
};

const processFetchIdAction = (next: Dispatch, storeDispatch: Dispatch, action: actions.Action) => {
  switch (action.payload.status) {
    case "start":
      next(action);
      fetchIdStart(storeDispatch);
      break;

    case "done":
      next(action);
      storeDispatch(timerActions.start());
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
      processFetchIdAction(next, store.dispatch, action);
      break;

    default:
      next(action);
  }
};

export default middleware;
