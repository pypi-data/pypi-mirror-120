import {Tooltip, Typography} from '@mui/material';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import IconButton from '@mui/material/IconButton';
import InputAdornment from '@mui/material/InputAdornment';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemSecondaryAction from '@mui/material/ListItemSecondaryAction';
import ListItemText from '@mui/material/ListItemText';
import Popover from '@mui/material/Popover';
import TextField from '@mui/material/TextField';
import ClearIcon from '@mui/icons-material/Clear';
import FolderOpenIcon from '@mui/icons-material/FolderOpen';
import InfoIcon from '@mui/icons-material/Info';
import {groupBy} from 'lodash';
import ReactMarkdown from 'markdown-to-jsx';
import React from 'react';
import {connect} from 'react-redux';
import {OPEN_DATASET_DIALOG, setDialog} from './actions';
import {NATSORT, REACT_MD_OVERRIDES} from './util';

export class DatasetSelector extends React.PureComponent {

    constructor(props) {
        super(props);
        this.state = {searchText: '', datasetDetailsEl: null, selectedDataset: null};
    }

    handleClick = (event) => {
        this.props.handleDialog(OPEN_DATASET_DIALOG);
        this.setState({searchText: ''});
    };

    handleClose = () => {
        this.props.handleDialog(null);
        this.setState({searchText: ''});
    };

    handleCloseDatasetDetails = (event) => {
        this.setState({datasetDetailsEl: null, selectedDataset: null});
    };

    handleListItemDetailsClick = (event, id) => {
        this.setState({datasetDetailsEl: event.currentTarget});
        this.props.serverInfo.api.getDatasetPromise(id).then(result => {
            this.setState({selectedDataset: result});
        });

    };

    handleListItemClick = (id) => {
        const selectedId = this.props.dataset != null ? this.props.dataset.id : null;
        if (id !== selectedId) {
            this.props.onChange(id);
        }
        this.props.handleDialog(null);
        this.setState({searchText: ''});
    };

    handleClearSearchText = () => {
        this.setState({searchText: ''});
    };

    onSearchChange = (event) => {
        this.setState({searchText: event.target.value});
    };

    render() {
        const {dataset, datasetChoices, dialog} = this.props;
        const selectedId = dataset != null ? dataset.id : null;

        if (datasetChoices.length <= 1 && selectedId != null) {
            return null;
        }
        const {searchText, selectedDataset} = this.state;
        const open = dialog === OPEN_DATASET_DIALOG;

        let filteredChoices = datasetChoices;
        const searchTextLower = this.state.searchText.toLowerCase().trim();
        if (searchTextLower != '') {
            filteredChoices = filteredChoices.filter(choice => choice.name.toLowerCase().indexOf(searchTextLower) !== -1 ||
                (choice.description != null && choice.description.toLowerCase().indexOf(searchTextLower) !== -1));
        }
        const datasetDetailsOpen = Boolean(this.state.datasetDetailsEl);
        const hasMoreInfo = selectedDataset && (selectedDataset.title || selectedDataset.description);
        const species2Items = groupBy(filteredChoices, item => item.species || '');
        const speciesArray = Object.keys(species2Items);
        speciesArray.sort(NATSORT);
        const otherIndex = speciesArray.indexOf("");
        if (otherIndex !== -1) { // move Other (empty string) to end
            speciesArray.push(speciesArray.splice(otherIndex, 1)[0]);
        }
        return (
            <React.Fragment>
                <Popover
                    id={"dataset-details-selector"}
                    open={datasetDetailsOpen}
                    anchorEl={this.state.datasetDetailsEl}
                    onClose={this.handleCloseDatasetDetails}
                    anchorOrigin={{
                        vertical: 'bottom',
                        horizontal: 'center'
                    }}
                    transformOrigin={{
                        vertical: 'top',
                        horizontal: 'center'
                    }}
                >
                    <div style={{width: 500}}>
                        {!hasMoreInfo && <div>No description available</div>}
                        {selectedDataset && selectedDataset.title && <div>{selectedDataset.title}</div>}
                        {selectedDataset && selectedDataset.description &&
                        <ReactMarkdown options={{overrides: REACT_MD_OVERRIDES}}
                                       children={selectedDataset.description}/>}
                    </div>
                </Popover>
                {selectedId == null && <Button variant="contained" onClick={this.handleClick}
                                               color="primary" startIcon={<FolderOpenIcon/>}>Open</Button>}
                {selectedId != null &&
                <Tooltip title={'Open'}><IconButton onClick={this.handleClick}
                                                    size="large"><FolderOpenIcon/></IconButton></Tooltip>}

                <Dialog
                    open={open}
                    onClose={this.handleClose}
                    fullWidth={true}
                >
                    <DialogContent style={{width: 500}}>
                        <TextField size="small" style={{padding: 6}} type="text" placeholder={"Search"}
                                   value={searchText}
                                   onChange={this.onSearchChange}
                                   fullWidth={true}
                                   InputProps={searchText.trim() !== '' ? {
                                       endAdornment:
                                           <InputAdornment position="end">
                                               <IconButton aria-label="clear" onClick={this.handleClearSearchText}
                                                           size="large">
                                                   <ClearIcon/>
                                               </IconButton>
                                           </InputAdornment>
                                   } : null}
                        />
                        <div style={{height: 500, overflow: 'auto'}}>
                            {speciesArray.length === 0 && searchText.trim() !== '' &&
                            <Typography>No Results</Typography>}
                            {speciesArray.map(species => {
                                const speciesText = species === '' ? 'Other' : species;
                                const choices = species2Items[species];
                                choices.sort((a, b) => NATSORT(a.name, b.name));
                                return (
                                    <React.Fragment key={species}>
                                        <Typography component={"h2"}>{speciesText}</Typography>
                                        <List dense disablePadding component="nav">
                                            {choices.map(choice => {
                                                let text = choice.name;
                                                if (choice.title) {
                                                    text += ' - ' + choice.title;
                                                }
                                                return (
                                                    <ListItem alignItems="flex-start"
                                                              selected={choice.id === selectedId}
                                                              key={choice.id}
                                                              button
                                                              onClick={(e) => this.handleListItemClick(choice.id)}>
                                                        <ListItemText
                                                            primary={text}
                                                            style={{
                                                                textOverflow: 'ellipsis',
                                                                overflow: 'hidden',
                                                                whiteSpace: 'nowrap'
                                                            }}/>
                                                        <ListItemSecondaryAction>
                                                            <IconButton
                                                                onClick={(e) => this.handleListItemDetailsClick(e, choice.id)}
                                                                edge="end"
                                                                aria-label="summary"
                                                                size="large">
                                                                <InfoIcon/>
                                                            </IconButton>
                                                        </ListItemSecondaryAction>
                                                    </ListItem>
                                                );
                                            })}
                                        </List></React.Fragment>
                                );
                            })}
                        </div>
                    </DialogContent>
                </Dialog>
            </React.Fragment>
        );
    }
}

const mapStateToProps = state => {
    return {
        dataset: state.dataset,
        dialog: state.dialog,
        datasetChoices: state.datasetChoices,
        serverInfo: state.serverInfo
    };
};
const mapDispatchToProps = dispatch => {
    return {
        handleDialog: value => {
            dispatch(setDialog(value));
        }

    };
};

export default (connect(
    mapStateToProps, mapDispatchToProps
)(DatasetSelector));

