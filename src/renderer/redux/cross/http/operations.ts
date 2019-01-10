import { Dispatch } from "redux";

import * as actions from "./actions";

import { actions as estimatorActions } from "../../state/estimator";

export const doneFetchedId = (dispatch: Dispatch, eid: number) => {
  dispatch(actions.fetchId("done"));
  dispatch(estimatorActions.setId(eid));
};
