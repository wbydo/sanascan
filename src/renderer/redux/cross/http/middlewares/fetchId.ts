import { Dispatch } from "redux";

import * as actions from "../actions";
import * as types from "../types";
import * as operations from "../operations";

import { Store } from "../../util";
import { actions as timerActions } from "../../timer";

import { setTimeoutPromise } from "../../../util";
import { url as baseUrl } from "../../../../constant";

import SanascanError from "../../../../error";

const TRY_NUMBER = 10;
const TIMEOUT = 5000;

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

const tryFethIdOnce = async (storeDispatch: Dispatch) => {
  const response = await fetch(baseUrl, {method: "POST"});
  const result = await response.json();

  if (result.eid !== undefined && typeof result.eid === "number") {
    operations.doneFetchedId(storeDispatch, result.eid as number);
    return;
  } else {
    throw new SanascanError();
  }
};

const processFetchIdAction = (next: Dispatch, action: ReturnType<typeof actions.fetchId>, storeDispatch: Dispatch) => {
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

export const middleware
    = (store: Store) => (next: Dispatch) => (action: ReturnType<typeof actions.fetchId>) => {

  switch (action.type) {
    case types.FETCH_ID:
      if (action.payload.status === undefined) {
        throw new SanascanError();
      }
      processFetchIdAction(next, action, store.dispatch);
      break;

    default:
      next(action);
  }
};
