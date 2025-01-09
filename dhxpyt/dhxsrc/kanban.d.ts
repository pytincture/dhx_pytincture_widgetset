declare namespace kanban{
type TDataBlock = {
    in: string[];
    out: string[];
    exec: any;
    length?: number;
};
type TDataConfig = TDataBlock[];
type TID$1 = number | string;
interface IEventConfig$1 {
    intercept?: boolean;
    tag?: number | string | symbol;
}
interface DataHash {
    [key: string]: any;
}
interface IWritable<T> {
    subscribe: (fn: (v: T) => any) => any;
    update: (fn: (v: T) => any) => any;
    set: (val: T) => any;
}
type TTrigger<T> = (v: T) => any;
type SomeCallback = () => void;
type TAsyncSignals = {
    [key: string]: SomeCallback | null;
};
interface IPublicWritable<T> {
    subscribe: (fn: TTrigger<T>) => any;
    __trigger(): void;
    __parse: (val: T, key: string, signals: TAsyncSignals, mode: TStateMode) => void;
}
type TWritableCreator = (val: any) => IWritable<typeof val>;
interface IEventBus$1<T> {
    exec(name: string, ev: T[keyof T]): Promise<T[keyof T]>;
    setNext(next: IEventBus$1<T>): IEventBus$1<T>;
}
type TStateMode = number;

class EventBus$1<T, A extends keyof T> {
    private _handlers;
    protected _nextHandler: IEventBus$1<T>;
    protected _tag: WeakMap<{
        (v: T[A]): void | boolean | Promise<boolean>;
    }, number | string | symbol>;
    constructor();
    on(name: A, handler: (v: T[A]) => void | boolean | Promise<boolean>, config?: IEventConfig$1): void;
    intercept(name: A, handler: (v: T[A]) => void | boolean | Promise<boolean>, config?: IEventConfig$1): void;
    detach(tag: number | string | symbol): void;
    exec(name: A, ev: T[A]): Promise<T[A]>;
    setNext(next: IEventBus$1<T>): IEventBus$1<T>;
}

type TState<Type> = {
    [Property in keyof Type]: IPublicWritable<Type[Property]>;
};
class Store<T extends DataHash> {
    private _state;
    private _values;
    private _writable;
    private _async;
    constructor(config: any);
    setState(data: Partial<T>, mode?: TStateMode | TDataConfig): TAsyncSignals;
    getState(): T;
    getReactive(): TState<T>;
    private _wrapProperties;
    private _wrapNested;
    private _wrapWritable;
}

function tempID(): string;

class ExportManager {
    private _store;
    constructor(store: DataStore);
    json(fileName?: string): void;
    private _save;
}

interface IMoveCardConfig {
    columnId: TID$1;
    rowId?: TID$1 | null;
    before?: TID$1 | null;
}

type THandlersFunction = {
    [Key in keyof THandlersConfig]: (store: DataStore, config?: THandlersConfig[Key]) => any;
};
interface ICoords {
    x: number;
    y: number;
}
interface IRect extends ICoords {
    top: number;
    bottom: number;
    left: number;
    right: number;
    width: number;
    height: number;
    id?: TID$1;
    scrollList?: IScrollColumn;
}
interface IScrollColumn {
    node: HTMLElement;
    initialScrollY: number;
}
interface IUser {
    id: TID$1;
    label?: string;
    avatar?: string;
    [key: string]: any;
}
interface ICard {
    id?: TID$1;
    label?: string;
    description?: string;
    progress?: number;
    users?: TID$1 | TID$1[];
    end_date?: Date | string;
    start_date?: Date | string;
    color?: string;
    priority?: any;
    attached?: IAttachment[];
    comments?: IComment[];
    votes?: TID$1[];
    css?: string;
    [key: string]: any;
}
interface INormalizedCard extends ICard {
    id: TID$1;
}
interface IAttachment {
    id?: TID$1;
    url?: string;
    previewURL?: string;
    coverURL?: string;
    file?: any;
    name?: string;
    status?: any;
    isCover?: boolean;
}
interface IRow {
    id: TID$1;
    label?: string;
    collapsed?: boolean;
    css?: string;
}
interface IColumn {
    id: TID$1;
    label?: string;
    limit?: number | Record<string, number>;
    strictLimit?: boolean;
    collapsed?: boolean;
    css?: string;
    overlay?: any;
}
type TAreaMeta = {
    columnId: TID$1;
    rowId?: TID$1;
    column: IColumn;
    row?: IRow;
    cardsCount: number;
    totalLimit?: number;
    isOverLimit?: boolean;
    noFreeSpace?: boolean;
    height?: number | null;
};
type TAreasMeta = Record<string, TAreaMeta>;
type TCardsMap = Record<string, INormalizedCard[] | undefined>;
interface ICardMeta {
    found?: boolean;
    dimmed?: boolean;
    dragging?: boolean;
}
type TScrollType = "default" | "column";
type TRenderType = "default" | "lazy";
type TLayoutType = "default:default" | "default:lazy" | "column:default" | "column:lazy";
interface IEditorConfig {
    autoSave?: boolean;
    debounce?: number;
    placement?: TEditorPlacement;
}
type TEditorPlacement = "sidebar" | "modal";
interface IKanbanEditorConfig extends IEditorConfig {
    show?: boolean;
}
interface IStoreConfig {
    history?: boolean;
}
interface IKanbanProps {
    cards: ICard[];
    columns: IColumn[];
    rows?: IRow[];
    cardShape?: TCardShape;
    columnShape?: IColumnShape;
    rowShape?: IRowShape;
    editorShape?: TEditorShape[];
    editor?: IKanbanEditorConfig;
    /** @deprecated use editor.autoSave instead */
    editorAutoSave?: boolean;
    cardTemplate?: any;
    readonly?: TReadonlyConfig;
    columnKey?: string;
    rowKey?: string;
    links?: ILink[];
    currentUser?: TID$1;
    scrollType?: TScrollType;
    renderType?: TRenderType;
    cardHeight?: number;
    api?: IApi;
    history?: boolean;
    dataStore?: DataStore;
}
interface IDataStoreState {
    columns: IColumn[];
    columnKey: string;
    rows: IRow[];
    rowKey?: string;
    cards: INormalizedCard[];
    cardsMap: TCardsMap;
    areasMeta: TAreasMeta;
    cardShape: ICardShape;
    editorShape?: TEditorShape[];
    columnShape?: IColumnShape;
    rowShape?: IRowShape;
    cardsMeta: Record<TID$1, ICardMeta | undefined>;
    links: ILink[];
    dragItemId: TID$1 | null;
    before: TID$1 | null;
    overAreaId?: TID$1 | null;
    dragItemsCoords: TDragItemsCoords | null;
    search: ISearchConfig | null;
    selected?: TID$1[] | null;
    scroll?: IScrollConfig | null;
    sort?: IAreaSortConfig | ISortConfig | null;
    edit?: IEditConfig | null;
    readonly?: IReadonlyModes | null;
    cardHeight?: number | null;
    layout: TLayoutType;
    history: IHistory;
    editor?: IKanbanEditorConfig;
    currentUser?: TID$1 | null;
}
interface IHistoryConfig {
    ev: THandlersConfig[keyof THandlersConfig];
    key: keyof THandlersConfig;
    undo: () => void;
}
interface IHistory {
    undo: (IHistoryConfig | number)[];
    redo: (Omit<IHistoryConfig, "undo"> | number)[];
    batches: Record<number, IHistoryConfig[]>;
}
interface IScrollConfig {
    id: TID$1 | undefined;
    to: "column" | "row" | "card";
    options?: ScrollIntoViewOptions;
}
type TSortDir = "asc" | "desc";
interface IAreaSortConfig {
    columns: Record<TID$1, ISortConfig | undefined>;
}
interface ISortConfig {
    by?: string | ((card: INormalizedCard) => any);
    dir?: TSortDir;
    preserve?: boolean;
}
interface ISortItemOption extends ISortConfig {
    /** @deprecated use text instead */
    label?: string;
    text: string;
    id?: TID$1;
    icon?: TWxIcons;
}
type TDropAreasCoords = IRect[];
type TDragItemsCoords = Record<string, IRect>;
type TSearchRule = (card: INormalizedCard, value: string, by?: string) => boolean;
interface ISearchConfig {
    value: string | null;
    by?: string;
    searchRule?: TSearchRule;
}
interface IMenuItem {
    id: string;
    icon?: TWxIcons;
    /** @deprecated use text instead */
    label?: string;
    text?: string;
    disabled?: boolean;
    /** @deprecated use data instead */
    items?: IMenuItem[];
    data?: IMenuItem[];
}
type TMenuItemsFn<T> = (config: T) => IMenuItem[] | null;
type TMenuItemsConfig<T> = IMenuItem[] | TMenuItemsFn<T> | null;
interface ICardField {
    show?: boolean;
    config?: Record<string, any>;
}
interface IComment {
    id: TID$1;
    userId: TID$1;
    cardId: TID$1;
    text: string;
    html?: string;
    date: Date;
}
interface ILink {
    id: TID$1;
    masterId: TID$1;
    slaveId: TID$1;
    relation: TRelationOptions;
}
interface ICardShape {
    label: ICardField;
    description?: ICardField;
    progress?: ICardField;
    start_date?: ICardField & {
        format?: string;
    };
    end_date?: ICardField & {
        format?: string;
    };
    menu?: {
        show?: boolean;
        items?: TMenuItemsConfig<{
            card: ICard;
        }>;
    };
    attached?: ICardField;
    users?: ICardField & {
        values?: IUser[];
    };
    priority?: ICardField & {
        values?: {
            id: TID$1;
            color: string;
            label?: string;
        }[];
    };
    color?: ICardField & {
        values?: string[];
    };
    cover?: ICardField;
    comments?: ICardField;
    headerFields?: {
        key: string;
        css?: string;
        label?: string;
    }[];
    css?: TCssProp;
    votes?: ICardField;
    confirmDeletion?: ICardField;
}
type TCssProp = (obj: any, cards?: INormalizedCard[]) => string;
type TCardShape = ObjectOrBoolean<ICardShape>;
type CombineTypes<T, N> = {
    [P in keyof T]: T[P] extends Record<any, any> ? T[P] & N : (T[P] & N) | null;
};
type ObjectOrBoolean<T> = {
    [P in keyof T]: T[P] | boolean;
};
interface IColumnShape {
    menu?: {
        show?: boolean;
        items?: TMenuItemsConfig<{
            column: IColumn;
            columns: IColumn[];
            columnIndex: number;
        }>;
    };
    css?: TCssProp;
    fixedHeaders?: boolean;
    confirmDeletion?: boolean;
    headerTemplate?: any;
    collapsedTemplate?: any;
}
type TColumnShape = ObjectOrBoolean<IColumnShape>;
interface IRowShape {
    menu?: {
        show?: boolean;
        items?: TMenuItemsConfig<{
            row: IRow;
            rows: IRow[];
            rowIndex: number;
        }>;
    };
    css?: TCssProp;
    confirmDeletion?: boolean;
}
type TRowShape = ObjectOrBoolean<IRowShape>;
interface IUploaderConfig {
    accept?: string;
    disabled?: boolean;
    multiple?: boolean;
    folder?: boolean;
}
type TCommonShape = {
    key: string | any;
    label?: string;
    id?: TID$1;
    modalSection?: "left" | "right";
};
type TTextFieldShape = TCommonShape & {
    type: "text";
    config?: {
        css?: string;
        disabled?: boolean;
        error?: boolean;
        focus?: boolean;
        icon?: string;
        inputStyle?: string;
        placeholder?: string;
        readonly?: boolean;
        select?: boolean;
        title?: string;
        type?: string;
    };
};
type TTitleFieldShape = TTextFieldShape;
type TTextAreaFieldShape = TCommonShape & {
    type: "textarea";
    config?: {
        disabled?: boolean;
        error?: boolean;
        placeholder?: string;
        title?: string;
        readonly?: boolean;
    };
};
type TProgressFieldShape = TCommonShape & {
    type: "progress";
    config?: {
        disabled?: boolean;
        label?: string;
        max?: number;
        min?: number;
        step?: number;
        title?: string;
        width?: number;
    };
};
type TMultiselectFieldShape = TCommonShape & {
    type: "multiselect";
    values?: IUser[];
    options?: IUser[];
    config?: {
        checkboxes?: boolean;
        disabled?: boolean;
        error?: boolean;
        placeholder?: string;
        textField?: string;
        title?: string;
    };
};
type TComboFieldShape = TCommonShape & {
    type: "combo";
    values?: {
        id: any;
        label?: string;
    }[];
    options?: {
        id: any;
        label?: string;
    }[];
    config?: {
        clearButton?: boolean;
        disabled?: boolean;
        error?: boolean;
        placeholder?: string;
        textField?: string;
        title?: string;
    };
};
type TSelectFieldShape = TCommonShape & {
    type: "select";
    values?: {
        id: any;
        label?: string;
    }[];
    options?: {
        id: any;
        label?: string;
    }[];
    config?: {
        disabled?: boolean;
        error?: boolean;
        label?: string;
        placeholder?: string;
        title?: string;
    };
};
type TColorFieldShape = TCommonShape & {
    type: "color";
    values?: string[];
    colors?: string[];
    config?: {
        clear?: boolean;
        disabled?: boolean;
        error?: boolean;
        placeholder?: string;
        title?: string;
    };
};
type TDateFieldShape = TCommonShape & {
    type: "date";
    format?: string;
    config?: {
        align?: "start" | "center" | "end";
        buttons?: boolean;
        css?: string;
        disabled?: boolean;
        error?: boolean;
        format?: string;
        placeholder?: string;
        title?: string;
        width?: string;
    };
};
type TDateRangeShape = TCommonShape & {
    type: "dateRange";
    format?: string;
    key: {
        start: TID$1;
        end: TID$1;
    };
    config?: {
        align?: "start" | "center" | "end";
        buttons?: boolean;
        css?: string;
        disabled?: boolean;
        done?: boolean;
        error?: boolean;
        format?: string;
        months?: number;
        placeholder?: string;
        title?: string;
        width?: string;
    };
};
type TFilesFieldShape = TCommonShape & {
    type: "files";
    uploadURL?: string;
    config?: IUploaderConfig;
};
type TCommentsShape = TCommonShape & {
    type: "comments";
    values?: IUser[];
    config?: {
        format?: string;
        placement?: "page" | "editor";
        html?: boolean;
        confirmDeletion?: boolean;
    };
};
type TLinksShape = TCommonShape & {
    type: "links";
    values?: ILink[];
    config?: {
        confirmDeletion?: boolean;
    };
};
type TEditorShape = TTextFieldShape | TTitleFieldShape | TTextAreaFieldShape | TMultiselectFieldShape | TComboFieldShape | TSelectFieldShape | TProgressFieldShape | TColorFieldShape | TDateFieldShape | TFilesFieldShape | TDateRangeShape | TCommentsShape | TLinksShape;
interface IReadonlyModes {
    edit?: boolean;
    add?: boolean;
    select?: boolean;
    dnd?: boolean;
}
type TReadonlyConfig = IReadonlyModes | boolean;
interface IApi {
    exec: (action: keyof THandlersConfig, params: any) => Promise<any>;
    on: (action: keyof THandlersConfig, callback: (config: any) => any) => void;
    intercept: (action: keyof THandlersConfig, callback: (config: any) => any) => void;
    getState: () => IDataStoreState;
    getReactiveState: () => {
        [Key in keyof IDataStoreState]: IPublicWritable<IDataStoreState[Key]>;
    };
    setNext: (ev: IEventBus$1<THandlersConfig>) => void;
    getStores: () => {
        data: DataStore;
    };
    getCard: (id: TID$1) => ICard | undefined;
    getAreaCards: (columnId: TID$1, rowId?: TID$1) => ICard[] | undefined;
    serialize: () => {
        cards: ICard[];
        links: ILink[];
        columns: IColumn[];
        rows?: IRow[] | null;
    };
    export: ExportManager;
    undo: () => void;
    redo: () => void;
}
interface ISearchOption {
    id: string | null;
    label?: string;
    searchRule?: TSearchRule;
}
type TItemTemplate = (config: Record<string, any>) => void[];
interface IToolbarDefaultItem {
    type: "addRow" | "addColumn" | "spacer" | "undo" | "redo";
}
interface ISearchItem {
    type: "search";
    options?: ISearchOption[];
    resultTemplate?: any;
}
interface ISortItem {
    type: "sort";
    options?: ISortItemOption[];
}
interface IEditConfig {
    cardId: TID$1;
}
interface ITemplateItem {
    type: "template";
    template?: TItemTemplate;
}
type IToolbarItem = IToolbarDefaultItem | ISearchItem | ISortItem | ITemplateItem;
type TWxIcons = "wxi-alert" | "wxi-angle-dbl-down" | "wxi-angle-dbl-left" | "wxi-angle-dbl-right" | "wxi-angle-dbl-up" | "wxi-angle-down" | "wxi-angle-left" | "wxi-angle-right" | "wxi-angle-up" | "wxi-arrow-down" | "wxi-arrow-left" | "wxi-arrow-right" | "wxi-arrow-up" | "wxi-arrows-h" | "wxi-arrows-v" | "wxi-asc" | "wxi-assign" | "wxi-bullhorn" | "wxi-calendar" | "wxi-camera" | "wxi-cat" | "wxi-check" | "wxi-clock" | "wxi-close" | "wxi-content-copy" | "wxi-content-cut" | "wxi-content-paste" | "wxi-convert" | "wxi-delete-outline" | "wxi-delete" | "wxi-desc" | "wxi-dots-h" | "wxi-dots-v" | "wxi-download" | "wxi-duplicate" | "wxi-earth" | "wxi-edit" | "wxi-edit-outline" | "wxi-emoticon-outline" | "wxi-empty" | "wxi-external" | "wxi-eye" | "wxi-file" | "wxi-filter-check" | "wxi-filter-outline" | "wxi-folder" | "wxi-food-fork-drink" | "wxi-human-handsdown" | "wxi-indent" | "wxi-information-outline" | "wxi-loading" | "wxi-menu-down" | "wxi-menu-right" | "wxi-paperclip" | "wxi-paste" | "wxi-pin-outline" | "wxi-plus" | "wxi-pound" | "wxi-redo" | "wxi-refresh" | "wxi-rename" | "wxi-search" | "wxi-soccer" | "wxi-sort" | "wxi-split" | "wxi-star-outline" | "wxi-subtask" | "wxi-table-column-plus-after" | "wxi-table-row-plus-after" | "wxi-table-row-plus-before" | "wxi-undo" | "wxi-unindent" | "wxi-upload" | "wxi-view-column" | "wxi-view-grid" | "wxi-view-sequential";
type TRelationOptions = "relatesTo" | "requiredFor" | "duplicate" | "parent";

class DataStore extends Store<IDataStoreState> {
    in: EventBus$1<THandlersConfig, keyof THandlersConfig>;
    out: EventBus$1<THandlersConfig, keyof THandlersConfig>;
    sortRule?: (config: ISortConfig) => (a: ICard, b: ICard) => number;
    config: IStoreConfig;
    private _router;
    constructor(w: TWritableCreator, config?: IStoreConfig);
    setState(state: Partial<IDataStoreState>, ctx?: any): TAsyncSignals;
    init(state: Partial<Omit<IDataStoreState, "cards" | "readonly" | "cardShape" | "columnShape" | "rowShape">> & {
        cards: ICard[];
        readonly: TReadonlyConfig;
        cardShape: TCardShape;
        columnShape: TColumnShape;
        rowShape: TRowShape;
    }): void;
    undo(): void;
    redo(): void;
    protected _setHandlers(handlersMap: THandlersFunction): void;
    protected _initStructure(): void;
    private _computeLimits;
    private _normalizeCards;
    private _normalizeShapes;
    private _normalizeReadonlyConfig;
}
type THandlersConfig = CombineTypes<{
    ["add-card"]: {
        id?: TID$1;
        card?: Partial<ICard>;
        select?: boolean;
    } & IMoveCardConfig;
    ["update-card"]: {
        id: TID$1;
        card: Partial<INormalizedCard>;
        replace?: boolean;
    };
    ["duplicate-card"]: {
        id: TID$1;
        card?: Partial<INormalizedCard>;
        select?: boolean;
    };
    ["delete-card"]: {
        id: TID$1;
    };
    ["move-card"]: {
        id: TID$1;
        card?: Partial<INormalizedCard>;
    } & IMoveCardConfig;
    ["add-column"]: {
        id?: TID$1;
        column?: Partial<IColumn>;
        before?: TID$1;
    };
    ["update-column"]: {
        id?: TID$1;
        column?: Partial<IColumn>;
        replace?: boolean;
    };
    ["move-column"]: {
        id?: TID$1;
        before?: TID$1;
    };
    ["delete-column"]: {
        id: TID$1;
    };
    ["add-row"]: {
        id?: TID$1;
        row?: Partial<IRow>;
        before?: TID$1;
    };
    ["update-row"]: {
        id?: TID$1;
        row?: Partial<IRow>;
        replace?: boolean;
    };
    ["move-row"]: {
        id?: TID$1;
        before?: TID$1;
    };
    ["delete-row"]: {
        id: TID$1;
    };
    ["set-search"]: ISearchConfig;
    ["start-drag-card"]: {
        id: TID$1;
        rowId?: TID$1 | null;
        columnId: TID$1;
        before?: TID$1 | null;
        source: TID$1[];
        dragItemsCoords: IDataStoreState["dragItemsCoords"] /** @deprecated will be removed in later versions */;
        dropAreasCoords: TDropAreasCoords | null /** @deprecated will be removed in later versions */;
    };
    ["drag-card"]: {
        id: TID$1;
        rowId?: TID$1 | null;
        columnId?: TID$1 | null;
        before?: TID$1 | null;
        source: TID$1[];
    };
    ["end-drag-card"]: {
        id: TID$1;
        rowId?: TID$1 | null;
        columnId?: TID$1 | null;
        before?: TID$1 | null;
        source: TID$1[];
    };
    ["select-card"]: {
        id: TID$1;
        groupMode?: boolean;
    };
    ["unselect-card"]: {
        id: TID$1 | null;
    };
    ["scroll"]: IScrollConfig;
    ["set-sort"]: (ISortConfig & {
        columnId?: TID$1;
    }) | null;
    ["set-edit"]: (IEditConfig & {
        eventSource?: string;
    }) | null;
    ["add-comment"]: {
        id?: TID$1;
        cardId: TID$1;
        comment: Partial<Omit<IComment, "userId">>;
    };
    ["update-comment"]: {
        id: TID$1;
        cardId: TID$1;
        comment: Partial<Omit<IComment, "userId">>;
    };
    ["delete-comment"]: {
        id: TID$1;
        cardId: TID$1;
    };
    ["add-link"]: {
        id?: TID$1;
        link: ILink;
    };
    ["delete-link"]: {
        id: TID$1;
    };
    ["add-vote"]: {
        cardId: TID$1;
    };
    ["delete-vote"]: {
        cardId: TID$1;
    };
}, {
    $meta?: {
        skipHistory?: boolean;
        batch?: number;
        restore?: TID$1;
    };
}>;

const defaultCardShape: ICardShape;
const defaultEditorShape: TEditorShape[];
const defaultEditorConfig: IKanbanEditorConfig;
const getDefaultCardMenuItems: ({ store }: {
    store: DataStore;
}) => {
    id: string;
    icon: string;
    text: string;
}[];
const getDefaultColumnMenuItems: ({ columns, columnIndex, }: {
    columns: IColumn[];
    columnIndex: number;
    store?: DataStore;
}) => ({
    id: string;
    icon: string;
    text: string;
    disabled?: undefined;
} | {
    id: string;
    icon: string;
    text: string;
    disabled: boolean;
})[];
const getDefaultRowMenuItems: ({ rows, rowIndex, }: {
    rows: IRow[];
    rowIndex: number;
    store?: DataStore;
}) => ({
    id: string;
    icon: string;
    text: string;
    disabled?: undefined;
} | {
    id: string;
    icon: string;
    text: string;
    disabled: boolean;
})[];

function locateID(el: Element | Event, attr?: string): string | number;

class Events {
    private _api;
    constructor(api: IApi);
    on<K extends keyof THandlersConfig>(event: K, callback: (config: THandlersConfig[K]) => any): void;
    exec<K extends keyof THandlersConfig>(event: K, data: THandlersConfig[K]): void;
}

type TThemeConfig = {
    name: string;
    fonts: boolean;
};
interface IKanbanConfig extends IKanbanProps {
    locale?: Record<string, any>;
    theme?: TThemeConfig;
}
class Kanban {
    api: IApi;
    export: ExportManager;
    events: Events;
    config: IKanbanConfig;
    container: HTMLElement;
    private _kanban;
    constructor(container: HTMLElement, config: IKanbanConfig);
    destructor(): void;
    setConfig(config: Partial<IKanbanConfig>): void;
    parse(data: {
        cards?: ICard[];
        links?: ILink[];
        columns?: IColumn[];
        rows?: IRow[];
    }): void;
    serialize(): {
        cards: INormalizedCard[];
        links: ILink[];
        columns: IColumn[];
        rows: IRow[];
    };
    undo(): void;
    redo(): void;
    getCard(id: TID$1): ICard;
    getAreaCards(columnId: TID$1, rowId?: TID$1): ICard[];
    getSelection(): TID$1[];
    addCard(config: THandlersConfig["add-card"]): void;
    updateCard(config: THandlersConfig["update-card"]): void;
    duplicateCard(config: THandlersConfig["duplicate-card"]): void;
    deleteCard(config: THandlersConfig["delete-card"]): void;
    moveCard(config: THandlersConfig["move-card"]): void;
    addColumn(config: THandlersConfig["add-column"]): void;
    updateColumn(config: THandlersConfig["update-column"]): void;
    addRow(config: THandlersConfig["add-row"]): void;
    updateRow(config: THandlersConfig["update-row"]): void;
    moveColumn(config: THandlersConfig["move-column"]): void;
    moveRow(config: THandlersConfig["move-row"]): void;
    deleteColumn(config: THandlersConfig["delete-column"]): void;
    deleteRow(config: THandlersConfig["delete-row"]): void;
    addLink(config: THandlersConfig["add-link"]): void;
    deleteLink(config: THandlersConfig["delete-link"]): void;
    addComment(config: THandlersConfig["add-comment"]): void;
    updateComment(config: THandlersConfig["update-comment"]): void;
    deleteComment(config: THandlersConfig["delete-comment"]): void;
    selectCard(config: THandlersConfig["select-card"]): void;
    unselectCard(config: THandlersConfig["unselect-card"]): void;
    setSearch(config: THandlersConfig["set-search"]): void;
    setSort(config: THandlersConfig["set-sort"]): void;
    setEdit(config: THandlersConfig["set-edit"]): void;
    scroll(config: THandlersConfig["scroll"]): void;
    setLocale(locale: Record<string, any>): void;
    setTheme(theme: TThemeConfig): void;
    private _init;
    private _reset;
    private _storeConfig;
    private _configToProps;
}
function template(template: any): (template: string | ((...x: any[]) => string)) => void;

interface IEditorProps {
    api: IApi;
    config?: IEditorConfig;
    shape?: TEditorShape[];
    locale?: Record<string, any>;
    theme?: string;
}
class Editor {
    api: IApi;
    config: IEditorProps;
    container: HTMLElement;
    events: Events;
    private _component;
    constructor(container: HTMLElement, config: IEditorProps);
    destructor(): void;
    setConfig(config: Partial<IEditorProps>): void;
    /** @version v1.5.7 */
    setLocale(locale: Record<string, any>, api?: IApi): void;
    private _init;
    private _configToProps;
}

interface IToolbarConfig {
    api: IApi;
    items?: string[] | TItemTemplate[] | IToolbarItem[];
    locale?: Record<string, any>;
    theme?: string;
}
class Toolbar {
    api: IApi;
    events: Events;
    config: IToolbarConfig;
    container: HTMLElement;
    private _toolbar;
    constructor(container: HTMLElement, config: IToolbarConfig);
    destructor(): void;
    setConfig(config: Partial<IToolbarConfig>): void;
    /** @version v1.5.7 */
    /** @version v2.0.0 api parameter is deprecated */
    setLocale(locale: Record<string, any>, api?: IApi): void;
    private _init;
    private _configToProps;
    private _normalizeItems;
}

interface IEventConfig {
    intercept?: boolean;
    tag?: number | string | symbol;
}
interface IEventBus<T> {
    exec(name: string, ev: T[keyof T]): Promise<T[keyof T]>;
    setNext(next: IEventBus<T>): IEventBus<T>;
}

class EventBus<T, A extends keyof T> {
    private _handlers;
    protected _nextHandler: IEventBus<T>;
    protected _tag: WeakMap<{
        (v: T[A]): void | boolean | Promise<boolean>;
    }, number | string | symbol>;
    constructor();
    on(name: A, handler: (v: T[A]) => void | boolean | Promise<boolean>, config?: IEventConfig): void;
    intercept(name: A, handler: (v: T[A]) => void | boolean | Promise<boolean>, config?: IEventConfig): void;
    detach(tag: number | string | symbol): void;
    exec(name: A, ev: T[A]): Promise<T[A]>;
    setNext(next: IEventBus<T>): IEventBus<T>;
}

type ActionHandler$1<T> = (ev: T) => Promise<any>;
type Action$1<T> = {
    ignoreID?: boolean;
    debounce?: number;
    handler: ActionHandler$1<T>;
};
type ActionMap$1<T> = {
    [P in keyof T]?: Action$1<T[P]>;
};
type DataObj = {
    [key: string]: any;
};
type TID = string | number;

class ActionQueue {
    private _awaitAddingQueue;
    private _queue;
    private _idPool;
    private _backId;
    private _status;
    private _waitPull;
    constructor();
    reset(ids?: boolean): void;
    resolve(id: TID, type: number): TID;
    getSync(): 0 | 1 | 2;
    waitSync(): Promise<void>;
    getId(id: TID): TID;
    waitId(id: TID): Promise<TID>;
    add(action: string, data: any, proc: any): Promise<boolean>;
    tryExec(action: string, data: DataObj, proc: any, finish?: () => void): boolean;
    exec(action: string, data: DataObj, proc: any, finish?: () => void): Promise<boolean> | null;
    correctID(obj: DataObj, ignore: TID): DataObj | symbol;
    execQueue(): void;
    private _finishQueue;
}

class Rest<T extends Record<any, any>> extends EventBus<T, keyof T> {
    private _queue;
    private _customHeaders;
    protected _url: string;
    constructor(url?: string);
    getHandlers(): ActionMap$1<T>;
    setHeaders(headers: any): void;
    getQueue(): ActionQueue;
    send<T>(url: string, method: string, data?: any, customHeaders?: any): Promise<T>;
}

type ActionHandler<T> = (ev: T) => Promise<any>;
type Action<T> = {
    kind?: number;
    ignoreID?: boolean;
    debounce?: number;
    handler: ActionHandler<T>;
};
type ActionMap<T> = {
    [P in keyof T]?: Action<T[P]>;
};
class RestDataProvider extends Rest<THandlersConfig> {
    constructor(url: string);
    getHandlers(): ActionMap<THandlersConfig>;
    getCards(): Promise<ICard[]>;
    getColumns(): Promise<IColumn[]>;
    getRows(): Promise<IRow[]>;
    getUsers(): Promise<IRow[]>;
    getLinks(): Promise<ILink[]>;
    getIDResolver(): any;
    send<T>(url: string, method: string, data?: string | object, customHeaders?: Record<string, string>): Promise<T>;
    protected parseCards(data: ICard[]): ICard[];
    protected prepareCard(card: ICard): {
        users: TID$1 | TID$1[];
        id?: TID$1;
        label?: string;
        description?: string;
        progress?: number;
        end_date?: string | Date;
        start_date?: string | Date;
        color?: string;
        priority?: any;
        attached?: IAttachment[];
        comments?: IComment[];
        votes?: TID$1[];
        css?: string;
    };
}

function kanbanUpdates(api: any, resolver: any): {
    cards: (obj: any) => void;
    columns: (obj: any) => void;
    rows: (obj: any) => void;
    links: (obj: any) => void;
};

class RemoteEvents {
    protected _remote: any;
    protected _ready: Promise<any>;
    constructor(url: string, token: string);
    protected ready(): Promise<any>;
    protected on(name: string | any, handler?: any): void;
}

export { Editor, Kanban, RemoteEvents, RestDataProvider, Toolbar, defaultCardShape, defaultEditorConfig, defaultEditorShape, getDefaultCardMenuItems, getDefaultColumnMenuItems, getDefaultRowMenuItems, kanbanUpdates, locateID, tempID, template };
}