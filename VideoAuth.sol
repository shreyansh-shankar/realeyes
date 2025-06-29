// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VideoAuth {
    struct Video {
        string videoHash;
        string uploader;
        uint timestamp;
    }

    mapping(string => Video) public videos;

    function registerVideo(string memory _videoHash, string memory _uploader) public {
        require(bytes(videos[_videoHash].videoHash).length == 0, "Video already registered.");
        videos[_videoHash] = Video(_videoHash, _uploader, block.timestamp);
    }

    function isVideoAuthentic(string memory _videoHash) public view returns (bool) {
        return bytes(videos[_videoHash].videoHash).length > 0;
    }

    function getVideoDetails(string memory _videoHash) public view returns (string memory, string memory, uint) {
        require(isVideoAuthentic(_videoHash), "Video not registered.");
        Video memory vid = videos[_videoHash];
        return (vid.videoHash, vid.uploader, vid.timestamp);
    }
}
