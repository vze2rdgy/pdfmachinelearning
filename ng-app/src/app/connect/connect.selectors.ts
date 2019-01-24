import { createSelector } from "@ngrx/store";
import { selectConnect, ConnectState } from "./connect.state";
import { ConnectTemlatesState } from "./templates/template.models";
import { Template } from "@angular/compiler/src/render3/r3_ast";

export const selectConnectTemplState = createSelector(
    selectConnect,
    (state: ConnectState) => state.templateState
)

export const selectTemplates = createSelector(
    selectConnectTemplState,
    (state: ConnectTemlatesState) => state.templatesResponse.templates
)