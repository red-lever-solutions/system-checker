/*jslint browser: true, devel: true*/
/*global WebSocket: false, Tipboard: false*/

function updateTileScrollableFancyListing(tileId, data, config, tipboard) {
    var tile = Tipboard.Dashboard.id2node(tileId);
    var nodeToClone = ScrollableFancyListing.initContainer(tile);
    if (nodeToClone === void 0) {
        return false;
    }
    ScrollableFancyListing.populateItems(tile, nodeToClone, data);
    ScrollableFancyListing.applyConfig(tile, config);
    Tipboard.TileDisplayDecorator.runAllDecorators(tile);
    if (config['vertical_center'] === true) {
        ScrollableFancyListing.verticalCenter(tile);
    }
}

Tipboard.Dashboard.registerUpdateFunction('scrollable_fancy_listing', updateTileScrollableFancyListing);

ScrollableFancyListing = {
    initContainer: function(tile) {
        var nodeToClone = $(tile).find('.scrollable-fancy-listing-item')[0];
        if (nodeToClone === void 0) {
            console.log('ABORTING - no node to clone');
            return false;
        }
        $(tile).find('.scrollable-fancy-listing-item').slice(1).remove();
        return nodeToClone;
    },
    appendCloned: function(tile, nodeToClone) {
        var container = $(tile).find('.tile-content')[0];
        $(nodeToClone).clone().appendTo(container);
    },
    populateItems: function(tile, clonedNode, data) {
        $.each(data, function(idx, tileData) {
            ScrollableFancyListing.appendCloned(tile, clonedNode);
            ScrollableFancyListing.replaceData(tile, tileData);
        });
    },
    applyConfig: function(tile, config) {
        $.each(config, function(idx, tileConfig) {
            if (/\d+/.test(idx)) {
                var item = $(tile).find('.scrollable-fancy-listing-item')[idx];
                // set color
                var color = Tipboard.DisplayUtils.replaceFromPalette(
                    tileConfig['label_color']
                );
                $(item).find('.scrollable-fancy-listing-label').css('background-color', color);
                // set centering
                if (tileConfig['center'] === true) {
                    $(item).find('.scrollable-fancy-listing-def').css(
                        'text-align', 'center'
                    );
                }
            }
        });
    },
    verticalCenter: function(tile) {
        // TODO: replace it with css class and toggle the class
        containerHeight = $(tile).find('.tile-content').height();
        children = $(tile).find('.tile-content').children().slice(1);
        var childrensHeight = 0;
        $.each(children, function(idx, child) {
            childrensHeight += $(child).outerHeight(true);
        });
        positionToSet = (containerHeight - childrensHeight) / 2;
        if (positionToSet > 0) {
            $(children[0]).css('padding-top', positionToSet);
        }
    },
    replaceData: function(tile, tileData) {
        var lastItem = $(tile).find('.scrollable-fancy-listing-item:last-child')[0];
        $(lastItem).find('.scrollable-fancy-listing-label-inside').html(tileData['label']);
        $(lastItem).find('.scrollable-fancy-listing-term').html(tileData['text']);
        $(lastItem).find('.scrollable-fancy-listing-desc').html(tileData['description']);
    }
};
